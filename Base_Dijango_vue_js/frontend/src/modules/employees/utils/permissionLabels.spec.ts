import { describe, expect, it } from "vitest";

import { permissionDescription, permissionLabel } from "./permissionLabels";

describe("permissionLabels", () => {
  it("presents Django permission codes in Vietnamese", () => {
    expect(permissionLabel("accounts.view_user")).toBe("Xem tài khoản người dùng");
    expect(permissionLabel("accounts.change_user")).toBe("Cập nhật tài khoản người dùng");
    expect(permissionDescription("accounts.add_user")).toBe(
      "Cho phép thêm tài khoản người dùng trong hệ thống.",
    );
  });
});
