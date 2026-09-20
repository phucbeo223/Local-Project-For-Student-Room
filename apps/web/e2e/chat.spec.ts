import { expect, test } from "@playwright/test";

const source = { kind: "legal_document", rank: 1, title: "Văn bản kiểm thử", heading: "Điều 3", page_from: 4, page_to: 5, excerpt: "Trích đoạn kiểm thử, chỉ mở khi yêu cầu." };

for (const width of [390, 1280]) {
  test(`chat concise answer, expandable sources and safe rendering (${width}px)`, async ({ page }) => {
    await page.setViewportSize({ width, height: 800 });
    await page.route("**/api/chat/ask", (route) => route.fulfill({ json: {
      answer: "**Kiểm tra hợp đồng trước khi đặt cọc.**\n- **Đọc điều kiện thuê [1]**.\n- *Đối chiếu nguồn*.\n<img src=x onerror=alert(1)>",
      listings: [], sources: [source], degraded: true, generation_provider: "template",
    } }));
    await page.goto("/login");
    await page.getByRole("button", { name: "Mở Trợ lý Trọ CTU" }).click();
    const widget = page.getByRole("region", { name: "Trợ lý tìm nhà trọ CTU" });
    await widget.getByPlaceholder("Tìm trọ hoặc hỏi quy định pháp luật...").fill("Quy định đặt cọc thuê trọ?");
    await widget.getByRole("button", { name: "Gửi câu hỏi" }).click();
    await expect(widget.locator("strong").first()).toHaveText("Kiểm tra hợp đồng trước khi đặt cọc.");
    await expect(widget.locator("em")).toHaveText("Đối chiếu nguồn");
    await expect(widget.locator("li")).toHaveCount(2);
    await expect(widget.getByText(source.title, { exact: false })).not.toBeVisible();
    await widget.getByRole("button", { name: "Xem nguồn 1" }).click();
    await expect(widget.getByText("[1] Văn bản kiểm thử")).toBeVisible();
    await expect(widget.getByText(source.excerpt)).not.toBeVisible();
    await widget.getByText("Đọc trích đoạn", { exact: true }).click();
    await expect(widget.getByText(source.excerpt)).toBeVisible();
    await expect(widget.locator("img")).toHaveCount(0);
    await expect(widget.getByText(/Vector chưa sẵn sàng/)).toHaveCount(0);
    await expect(widget.getByRole("heading", { name: "Trợ lý Trọ CTU" })).toBeVisible();
    expect(await widget.evaluate((el) => el.scrollWidth <= el.clientWidth)).toBeTruthy();
    await page.screenshot({ path: `test-results/chat-${width}.png` });
    await widget.getByTitle("Phóng to").click();
    await expect(widget.getByTitle("Thu nhỏ")).toBeVisible();
  });
}

test("long answers remain available and follow-up history fits API limit", async ({ page }) => {
  const answer = "Thông tin tham khảo.\n" + "- Nội dung kiểm thử dài, cần đọc đầy đủ trước khi quyết định.\n".repeat(50) + "KẾT THÚC [1]";
  let calls = 0;
  await page.route("**/api/chat/ask", (route) => {
    const body = route.request().postDataJSON();
    if (++calls === 2) expect(body.conversation_history.every((turn: { content: string }) => turn.content.length <= 2000)).toBeTruthy();
    return route.fulfill({ json: { answer, listings: [], sources: [source], degraded: false, generation_provider: "qwen-local", generation_model: "qwen3.5:4b" } });
  });
  await page.goto("/login");
  await page.getByRole("button", { name: "Mở Trợ lý Trọ CTU" }).click();
  const input = page.getByPlaceholder("Tìm trọ hoặc hỏi quy định pháp luật...");
  await input.fill("Quy định hợp đồng thuê trọ?");
  await page.getByRole("button", { name: "Gửi câu hỏi" }).click();
  await expect(page.getByText("KẾT THÚC", { exact: false })).not.toBeVisible();
  expect((await page.getByTestId("chat-answer").last().innerText()).length).toBeLessThan(450);
  await page.getByRole("button", { name: "Xem toàn bộ câu trả lời" }).click();
  await expect(page.getByText("KẾT THÚC", { exact: false })).toBeVisible();
  await page.getByRole("button", { name: "Thu gọn câu trả lời" }).click();
  await input.fill("Còn tiền điện thì sao?");
  await page.getByRole("button", { name: "Gửi câu hỏi" }).click();
  await expect(page.getByRole("button", { name: "Xem toàn bộ câu trả lời" })).toHaveCount(2);
  expect(calls).toBe(2);
});
