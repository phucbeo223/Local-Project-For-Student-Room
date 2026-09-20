import { test, expect } from "@playwright/test";

test("map loads compact results and routes through the same-origin proxy", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.route("**/api/listings/*/route-path?campus=*", (route) =>
    route.fulfill({ json: [[10.0322, 105.7683], [10.035, 105.77]] }),
  );
  await page.goto("/map");
  await expect(page.getByRole("heading", { name: /\d+ tin trong bán kính/ })).toBeVisible();
  await expect(page.getByRole("button", { name: "Khu II", exact: true })).toBeVisible();
  await expect(page.locator(".leaflet-marker-icon").first()).toBeVisible();

  const firstListing = page.locator("aside button").filter({ has: page.locator("span.line-clamp-2") }).first();
  await expect(firstListing).toBeVisible();
  const routeResponse = page.waitForResponse((response) =>
    response.url().includes("/route-path?campus=1") && response.status() === 200,
  );
  await firstListing.click();
  await routeResponse;
  await expect(page.getByRole("link", { name: "Xem chi tiết", exact: true })).toBeVisible();
  await expect(page.locator('.leaflet-overlay-pane path[stroke="#1069bd"][stroke-width="4"]')).toBeVisible();
  await page.getByRole("button", { name: "Đóng", exact: true }).click();
  await expect(page.getByRole("link", { name: "Xem chi tiết", exact: true })).toHaveCount(0);
  expect(errors).toEqual([]);
});
