import type { Router } from "vue-router";

import { bootstrapAuth, roleHomePath } from "@/modules/auth/composables/useAuth";
import { useAuthStore } from "@/modules/auth/stores/auth";

export function installRouterGuards(router: Router) {
  router.beforeEach(async (to) => {
    const auth = useAuthStore();
    await bootstrapAuth();

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
      return { name: "login", query: { redirect: to.fullPath } };
    }
    if (to.meta.guestOnly && auth.user) return roleHomePath(auth.user.role);
    if (auth.user && to.meta.roles && !to.meta.roles.includes(auth.user.role)) {
      return { name: "forbidden" };
    }
    if (
      auth.user &&
      to.meta.permissions &&
      !to.meta.permissions.every((permission) => auth.user?.permissions.includes(permission))
    ) {
      return { name: "forbidden" };
    }
    return true;
  });
}
