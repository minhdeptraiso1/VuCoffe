export type UserRole = "admin" | "employee" | "customer";

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  date_joined: string;
  role: UserRole;
  permissions: string[];
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  user: User;
}

export interface RegisterCredentials {
  email: string;
  full_name: string;
  password: string;
}

export interface RefreshResponse {
  access: string;
}
