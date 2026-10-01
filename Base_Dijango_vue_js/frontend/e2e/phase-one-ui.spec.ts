import { expect, test } from "@playwright/test";

test("home and menu share the same stable public header", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  for (const path of ["/", "/menu"]) {
    await page.goto(path);
    const header = page.locator("header").first();
    await expect(header).toBeVisible();
    await expect(header).toHaveCSS("height", "72px");
    await expect(header.getByRole("link", { name: "Trang chủ", exact: true })).toBeVisible();
    await expect(header.getByRole("link", { name: "Thực đơn", exact: true })).toBeVisible();
    const navItemsDoNotWrap = await page.evaluate<boolean>(
      "Array.from(document.querySelector('header nav').querySelectorAll('a')).every((item) => getComputedStyle(item).whiteSpace === 'nowrap')",
    );
    expect(navItemsDoNotWrap).toBe(true);
  }
});

test("public header switches to mobile navigation without overflow", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto("/");
  await page.getByRole("button", { name: "Mở menu" }).click();
  await expect(page.getByRole("navigation", { name: "Điều hướng di động" })).toBeVisible();
  const hasNoOverflow = await page.evaluate<boolean>(
    "document.documentElement.scrollWidth <= window.innerWidth",
  );
  expect(hasNoOverflow).toBe(true);
});

test("design system showcase is no longer exposed", async ({ page }) => {
  await page.goto("/design-system");
  await expect(page.getByRole("heading", { name: "Không tìm thấy trang" })).toBeVisible();
});

test("landing and menu keep content focused", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Món đặc sản" })).toHaveCount(0);
  await expect(page.getByRole("link", { name: /Khám phá toàn bộ thực đơn/ })).toHaveCount(0);
  await expect(
    page.getByRole("heading", { name: "Một quán cà phê làm bằng sự tử tế" }),
  ).toBeVisible();

  await page.goto("/menu");
  await expect(page.getByRole("heading", { name: "Thực đơn", exact: true })).toBeVisible();
  await expect(page.locator("[data-menu-sheet]")).toBeVisible();
  await expect(page.locator("[data-menu-sheet] img")).toHaveCount(15);
  await expect(page.getByLabel("Tìm món trong thực đơn")).toBeVisible();
});
