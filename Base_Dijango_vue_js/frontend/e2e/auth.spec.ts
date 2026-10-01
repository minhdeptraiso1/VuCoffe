import { expect, test } from "@playwright/test";

test("CSRF, HttpOnly cookie, reload, profile and logout", async ({ page, context }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill(process.env.E2E_USER_EMAIL || "demo@example.com");
  await page.locator('input[name="password"]').fill(process.env.E2E_USER_PASSWORD || "123456");
  await page.getByRole("button", { name: "Đăng nhập", exact: true }).click();
  await expect(page).toHaveURL(/\/account$/);

  const refreshCookie = (await context.cookies()).find((cookie) => cookie.name === "refresh_token");
  expect(refreshCookie?.httpOnly).toBe(true);
  expect(
    await page.evaluate(() => ({ local: localStorage.length, session: sessionStorage.length })),
  ).toEqual({
    local: 0,
    session: 0,
  });

  await page.reload();
  await expect(
    page.getByRole("heading", { name: "Chào mừng bạn đến với Kim Thành Coffee" }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Hồ sơ cá nhân" }).click();
  await page.getByLabel("Họ và tên").fill("Người dùng thử");
  await page.getByRole("button", { name: "Lưu thay đổi" }).click();
  await expect(page.getByText("Đã cập nhật hồ sơ.")).toBeVisible();

  await page.getByRole("button", { name: "Đăng xuất" }).click();
  await expect(page).toHaveURL(/\/login$/);
  await page.reload();
  await expect(page).toHaveURL(/\/login$/);
});

test("public landing keeps primary actions and hero visual usable", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Khám phá nghệ thuật/ })).toBeVisible();
  await expect(page.getByRole("link", { name: "Đặt món ngay" })).toHaveAttribute("href", "/menu");
  await expect(page.getByAltText(/Tách cà phê Kim Thành/)).toBeVisible();
});

test("landing has no horizontal overflow at target breakpoints and respects reduced motion", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  for (const width of [375, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    await expect(page.getByRole("link", { name: "Đặt món ngay" })).toBeVisible();
    const hasNoOverflow = await page.evaluate<boolean>(
      "document.documentElement.scrollWidth <= window.innerWidth",
    );
    expect(hasNoOverflow).toBe(true);
  }
  await expect(page.locator("canvas")).toHaveCount(0);
});

test("admin and employee enter the correct management workspace", async ({ page, isMobile }) => {
  test.skip(isMobile, "Role management smoke test runs once on desktop.");

  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@example.com");
  await page.locator('input[name="password"]').fill("123456");
  await page.getByRole("button", { name: "Đăng nhập", exact: true }).click();
  await expect(page).toHaveURL(/\/admin$/);
  await expect(page.getByRole("navigation", { name: "Điều hướng quản lý" })).toBeVisible();

  await page.getByRole("link", { name: "Nhân viên", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Quản lý nhân viên" })).toBeVisible();
  const firstPermissionButton = page.getByRole("button", { name: "Phân quyền" }).first();
  if (await firstPermissionButton.isVisible()) {
    await firstPermissionButton.click();
    await expect(page.getByText("Xem tài khoản người dùng", { exact: true })).toBeVisible();
    await expect(page.getByText(/accounts\.|Can view user/)).toHaveCount(0);
    await page.keyboard.press("Escape");
  }

  await page.getByRole("button", { name: "Đăng xuất" }).click();
  await page.getByLabel("Email").fill("employee@example.com");
  await page.locator('input[name="password"]').fill("123456");
  await page.getByRole("button", { name: "Đăng nhập", exact: true }).click();
  await expect(page).toHaveURL(/\/employee$/);
  await expect(page.getByRole("heading", { name: /Xin chào/ })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Điều hướng quản lý" })).toBeVisible();
});
