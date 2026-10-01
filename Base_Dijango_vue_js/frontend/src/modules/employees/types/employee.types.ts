import type { User } from "@/modules/auth/types";

export interface PaginatedEmployees {
  count: number;
  next: string | null;
  previous: string | null;
  results: User[];
}

export interface PermissionOption {
  code: string;
  name: string;
}

export interface CreateEmployeeInput {
  email: string;
  full_name: string;
  password: string;
}
