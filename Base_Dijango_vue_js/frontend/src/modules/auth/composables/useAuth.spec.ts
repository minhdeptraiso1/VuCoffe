import { describe, expect, it } from "vitest";

import { roleHomePath } from "./useAuth";

describe("roleHomePath", () => {
  it("routes every role to its own workspace", () => {
    expect(roleHomePath("admin")).toBe("/admin");
    expect(roleHomePath("employee")).toBe("/employee");
    expect(roleHomePath("customer")).toBe("/account");
  });
});
