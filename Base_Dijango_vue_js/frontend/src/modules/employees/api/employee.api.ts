import { apiClient } from "@/lib/http/client";
import type { User } from "@/modules/auth/types";
import type {
  CreateEmployeeInput,
  PaginatedEmployees,
  PermissionOption,
} from "../types/employee.types";

export async function employeesRequest(page = 1): Promise<PaginatedEmployees> {
  return (await apiClient.get<PaginatedEmployees>("/api/v1/auth/employees/", { params: { page } }))
    .data;
}

export async function createEmployeeRequest(input: CreateEmployeeInput): Promise<User> {
  return (await apiClient.post<User>("/api/v1/auth/employees/", input)).data;
}

export async function permissionCatalogRequest(): Promise<PermissionOption[]> {
  return (await apiClient.get<PermissionOption[]>("/api/v1/auth/permissions/")).data;
}

export async function updateEmployeePermissionsRequest(
  employeeId: number,
  permissions: string[],
): Promise<User> {
  return (
    await apiClient.patch<User>(`/api/v1/auth/employees/${String(employeeId)}/permissions/`, {
      permissions,
    })
  ).data;
}
