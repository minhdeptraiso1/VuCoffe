import { expect, test } from "@playwright/test";

test("menu search, customization and cart remain usable", async ({ page }) => {
  await page.goto("/menu");
  await expect(page.getByRole("heading", { name: "Thực đơn", exact: true })).toBeVisible();
  await expect(page.locator("[data-menu-sheet]")).toBeVisible();
  await expect(page.getByRole("button", { name: /Món đặc sản/ })).toHaveCount(0);

  await page.getByLabel("Tìm món trong thực đơn").fill("không có món này");
  await expect(page.getByRole("heading", { name: "Không tìm thấy món phù hợp" })).toBeVisible();
  await page.getByRole("button", { name: "Xem toàn bộ thực đơn" }).click();

  await page.getByRole("button", { name: /Tùy chỉnh Cà phê Muối Kim Thành/ }).click();
  await expect(page.getByRole("dialog", { name: "Tùy chỉnh món" })).toBeVisible();
  await page.getByRole("button", { name: "50% đường" }).click();
  await page.getByRole("button", { name: "Thêm vào giỏ" }).click();

  await page
    .getByRole("button", { name: /Giỏ hàng/ })
    .first()
    .click();
  await expect(page.getByRole("dialog", { name: "Giỏ hàng của bạn" })).toBeVisible();
  await expect(
    page
      .getByRole("list", { name: "Các món trong giỏ hàng" })
      .getByRole("heading", { name: "Cà phê Muối Kim Thành" }),
  ).toBeVisible();
  await expect(page.getByText("Đặt hàng trực tuyến sắp mở")).toBeVisible();
});

test("menu has no horizontal page overflow at target widths", async ({ page }) => {
  for (const width of [375, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/menu");
    await expect(page.getByLabel("Tìm món trong thực đơn")).toBeVisible();
    const hasNoOverflow = await page.evaluate<boolean>(
      "document.documentElement.scrollWidth <= window.innerWidth",
    );
    expect(hasNoOverflow, `Viewport ${String(width)}px must not overflow`).toBe(true);
  }
});
