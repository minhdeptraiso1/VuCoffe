import { createPinia, setActivePinia } from "pinia";
import { flushPromises, mount } from "@vue/test-utils";
import { ref } from "vue";
import { createMemoryHistory, createRouter } from "vue-router";
import { vi } from "vitest";

import { useToastStore } from "@/app/stores/toast";

import LoginPage from "./LoginPage.vue";

const login = vi.fn<() => Promise<void>>().mockResolvedValue(undefined);

vi.mock("../composables/useAuth", () => ({
  useAuth: () => ({
    login,
    logout: vi.fn(),
    loginLoading: ref(false),
    logoutLoading: ref(false),
  }),
}));

describe("LoginPage", () => {
  beforeEach(() => {
    login.mockReset().mockResolvedValue(undefined);
  });

  it("renders accessible, browser-assisted login fields", async () => {
    const pinia = createPinia();
    setActivePinia(pinia);
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: "/login", component: LoginPage }],
    });
    await router.push("/login");
    await router.isReady();

    const wrapper = mount(LoginPage, { global: { plugins: [pinia, router] } });
    expect(wrapper.get('input[name="email"]').attributes("autocomplete")).toBe("email");
    expect(wrapper.get('input[name="password"]').attributes("autocomplete")).toBe(
      "current-password",
    );

    expect(wrapper.get('input[name="email"]').attributes("required")).toBeDefined();
    expect(wrapper.get('input[name="password"]').attributes("required")).toBeDefined();
    expect(login).not.toHaveBeenCalled();
  });

  it("shows an error toast when the API rejects the credentials", async () => {
    login.mockRejectedValueOnce({
      isAxiosError: true,
      response: { status: 401, data: { code: "invalid_credentials" } },
    });
    const pinia = createPinia();
    setActivePinia(pinia);
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: "/login", component: LoginPage }],
    });
    await router.push("/login");
    await router.isReady();

    const wrapper = mount(LoginPage, { global: { plugins: [pinia, router] } });
    await wrapper.get('input[name="email"]').setValue("sai@example.com");
    await wrapper.get('input[name="password"]').setValue("mat-khau-sai");
    await wrapper.get("form").trigger("submit");
    await flushPromises();

    await vi.waitFor(() => {
      expect(login).toHaveBeenCalledOnce();
    });
    await vi.waitFor(() => {
      expect(useToastStore().message).toBe("Email hoặc mật khẩu không đúng.");
    });
    expect(useToastStore().variant).toBe("error");
  });
});
