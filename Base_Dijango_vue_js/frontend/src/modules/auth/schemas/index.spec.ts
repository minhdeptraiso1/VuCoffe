import { loginValuesSchema, registerValuesSchema } from ".";

describe("loginValuesSchema", () => {
  it("rejects malformed email and an empty password", () => {
    const result = loginValuesSchema.safeParse({ email: "not-an-email", password: "" });
    expect(result.success).toBe(false);
    if (result.success) return;
    expect(result.error.flatten().fieldErrors.email).toContain("Email chưa đúng định dạng.");
    expect(result.error.flatten().fieldErrors.password).toContain("Vui lòng nhập mật khẩu.");
  });
});

describe("registerValuesSchema", () => {
  it("requires matching passwords", () => {
    const result = registerValuesSchema.safeParse({
      full_name: "Khách hàng",
      email: "customer@example.com",
      password: "StrongPass!123",
      confirm_password: "DifferentPass!123",
    });
    expect(result.success).toBe(false);
    if (result.success) return;
    expect(result.error.flatten().fieldErrors.confirm_password).toContain(
      "Mật khẩu nhập lại chưa khớp.",
    );
  });
});
