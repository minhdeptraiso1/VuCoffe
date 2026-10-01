import { storeToRefs } from "pinia";
import { ref } from "vue";
import { useRouter } from "vue-router";

import { useToastStore } from "@/app/stores/toast";
import { toAppError } from "@/lib/http/errors";

import { loginRequest, logoutRequest, meRequest, registerRequest } from "../api";
import { useAuthStore } from "../stores/auth";
import type { LoginCredentials, RegisterCredentials, UserRole } from "../types";
import { broadcastAuthEvent, withAuthLock } from "./coordination";
import { refreshAccessToken } from "./refresh";

let bootstrapFlight: Promise<void> | null = null;

export function roleHomePath(role: UserRole): string {
  if (role === "admin") return "/admin";
  if (role === "employee") return "/employee";
  return "/account";
}

export function bootstrapAuth(): Promise<void> {
  const auth = useAuthStore();
  if (auth.bootstrapState === "ready") return Promise.resolve();
  if (bootstrapFlight) return bootstrapFlight;

  auth.bootstrapState = "loading";
  bootstrapFlight = (async () => {
    if (auth.logoutPending) return;
    try {
      const accessToken = await refreshAccessToken();
      auth.setSession(await meRequest(), accessToken);
    } catch (error) {
      auth.clearSession();
      const appError = toAppError(error);
      if (appError.kind === "network" || appError.kind === "server") {
        auth.bootstrapError = appError.message;
      }
    } finally {
      auth.bootstrapState = "ready";
      bootstrapFlight = null;
    }
  })();
  return bootstrapFlight;
}

export function useAuth() {
  const auth = useAuthStore();
  const toast = useToastStore();
  const router = useRouter();
  const { user, isAuthenticated, logoutError } = storeToRefs(auth);
  const loginLoading = ref(false);
  const logoutLoading = ref(false);

  async function login(credentials: LoginCredentials, redirect?: string) {
    loginLoading.value = true;
    try {
      const response = await loginRequest(credentials);
      auth.setSession(response.user, response.access);
      toast.show("Đăng nhập thành công.", "success");
      await router.replace(redirect ?? roleHomePath(response.user.role));
    } finally {
      loginLoading.value = false;
    }
  }

  async function register(credentials: RegisterCredentials) {
    loginLoading.value = true;
    try {
      const response = await registerRequest(credentials);
      auth.setSession(response.user, response.access);
      toast.show("Đã tạo tài khoản thành công.", "success");
      await router.replace(roleHomePath(response.user.role));
    } finally {
      loginLoading.value = false;
    }
  }

  async function logout() {
    auth.clearSession();
    auth.markLogoutPending(true);
    auth.logoutError = "";
    await router.replace({ name: "login" });
    logoutLoading.value = true;
    try {
      await withAuthLock(logoutRequest);
      auth.markLogoutPending(false);
      broadcastAuthEvent({ type: "logout" });
      toast.show("Đã đăng xuất an toàn.", "success");
    } catch (error) {
      auth.logoutError = toAppError(error).message;
      toast.show(auth.logoutError, "error");
    } finally {
      logoutLoading.value = false;
    }
  }

  return {
    user,
    isAuthenticated,
    loginLoading,
    logoutLoading,
    logoutError,
    login,
    register,
    logout,
  };
}
