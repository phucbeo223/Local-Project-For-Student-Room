import { expect, test } from "@playwright/test";

// Opt in: calls the real local model and records normal chat metrics.
test("Qwen local answers through the deployed UI with real sources", async ({ page }) => {
  test.skip(process.env.QWEN_SMOKE !== "1", "Requires deployed API, Ollama and demo account");
  test.setTimeout(240_000);
  await page.goto("/login");
  await page.getByLabel("Email").fill(process.env.E2E_EMAIL ?? "nguyenvana@ctu.edu.vn");
  await page.getByLabel("Mật khẩu").fill(process.env.E2E_PASSWORD ?? "123456");
  await page.getByRole("button", { name: "Đăng nhập", exact: true }).click();
  await expect(page).toHaveURL(/\/$/);
  await page.goto("/chat");
  const widget = page.getByRole("region", { name: "Trợ lý tìm nhà trọ CTU" });
  for (const question of ["Tìm phòng trọ dưới 2 triệu gần CTU", "Chủ trọ được thu tiền điện như thế nào theo quy định?"]) {
    await widget.getByPlaceholder("Tìm trọ hoặc hỏi quy định pháp luật...").fill(question);
    const pending = page.waitForResponse("**/api/chat/ask", { timeout: 120_000 });
    await widget.getByRole("button", { name: "Gửi câu hỏi" }).click();
    const response = await pending;
    expect(response.ok()).toBeTruthy();
    const result = await response.json();
    console.log(JSON.stringify({ question, provider: result.generation_provider, model: result.generation_model,
      retrieval: result.retrieval_mode, latency_ms: result.latency_ms, degraded: result.degraded,
      reasons: result.degraded_reasons, sources: result.sources.length, answer: result.answer }));
    expect(result.generation_provider).toBe("qwen-local");
    expect(result.generation_model).toBe("qwen3.5:4b");
    expect(result.degraded).toBe(false);
    expect(result.sources.length).toBeGreaterThan(0);
    expect(result.citation_accuracy).toBe(1);
    await expect(widget.getByText(/AI: Qwen local/).last()).toBeAttached();
    await expect(widget.getByTestId("chat-answer").last().locator("p").first()).toBeInViewport();
  }
  await page.screenshot({ path: "test-results/chat-qwen-live.png" });
  await expect(widget.getByRole("heading", { name: "Trợ lý Trọ CTU" })).toBeVisible();
  await widget.getByTitle("Phóng to").click();
  await expect(widget.getByTitle("Thu nhỏ")).toBeVisible();
});
