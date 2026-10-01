import { vi } from "vitest";

const client = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn(), patch: vi.fn() }));
vi.mock("@/lib/http/client", () => ({ apiClient: client }));

import {
  createEmployeeRequest,
  employeesRequest,
  permissionCatalogRequest,
  updateEmployeePermissionsRequest,
} from "./employee.api";

describe("employee API", () => {
  it("uses the admin employee and permission contracts", async () => {
    client.get.mockResolvedValueOnce({
      data: { count: 0, next: null, previous: null, results: [] },
    });
    await employeesRequest(2);
    expect(client.get).toHaveBeenLastCalledWith("/api/v1/auth/employees/", { params: { page: 2 } });

    client.get.mockResolvedValueOnce({ data: [] });
    await permissionCatalogRequest();
    expect(client.get).toHaveBeenLastCalledWith("/api/v1/auth/permissions/");

    const input = {
      email: "staff@example.com",
      full_name: "Nhân viên",
      password: "StrongPass!123",
    };
    client.post.mockResolvedValueOnce({ data: { id: 7 } });
    await createEmployeeRequest(input);
    expect(client.post).toHaveBeenCalledWith("/api/v1/auth/employees/", input);

    client.patch.mockResolvedValueOnce({ data: { id: 7 } });
    await updateEmployeePermissionsRequest(7, ["accounts.view_user"]);
    expect(client.patch).toHaveBeenCalledWith("/api/v1/auth/employees/7/permissions/", {
      permissions: ["accounts.view_user"],
    });
  });
});
