<script setup lang="ts">
import { computed, ref, type Component } from "vue";
import {
  Database,
  FileSpreadsheet,
  House,
  LayoutDashboard,
  LogOut,
  Menu,
  PackageOpen,
  UserRound,
  UsersRound,
  X,
} from "lucide-vue-next";
import { useRoute } from "vue-router";

import BaseButton from "@/components/base/BaseButton.vue";
import AppLogo from "@/components/brand/AppLogo.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import { useAuth } from "@/modules/auth/composables/useAuth";

interface NavItem {
  label: string;
  to: string;
}
interface Props {
  eyebrow: string;
  home: string;
  navigation: NavItem[];
}
const props = defineProps<Props>();
const route = useRoute();
const mobileOpen = ref(false);
const { user, logout, logoutLoading, logoutError } = useAuth();
const roleLabel = computed(() =>
  props.eyebrow === "Quản trị" ? "Không gian quản trị" : "Không gian nhân viên",
);
function navIcon(to: string): Component {
  if (to.includes("employees")) return UsersRound;
  if (to.includes("catalog")) return PackageOpen;
  if (to.includes("inventory")) return Database;
  if (to.includes("imports")) return FileSpreadsheet;
  if (to === "/profile") return UserRound;
  return LayoutDashboard;
}
function isActive(to: string) {
  return route.path === to;
}
</script>

<template>
  <div class="min-h-screen bg-[var(--color-background)] lg:grid lg:grid-cols-[264px_minmax(0,1fr)]">
    <button
      v-if="mobileOpen"
      type="button"
      class="fixed inset-0 z-30 bg-[var(--color-overlay)] lg:hidden"
      aria-label="Đóng thanh điều hướng"
      @click="mobileOpen = false"
    ></button>
    <aside
      class="fixed inset-y-0 left-0 z-40 flex w-[264px] -translate-x-full flex-col border-r border-white/10 bg-[var(--color-espresso-dark)] text-white transition-transform lg:sticky lg:top-0 lg:h-screen lg:translate-x-0"
      :class="mobileOpen && 'translate-x-0'"
    >
      <div class="flex h-[72px] items-center justify-between border-b border-white/10 px-5">
        <RouterLink :to="props.home" aria-label="Về trang tổng quan"
          ><AppLogo variant="pill" size="md"
        /></RouterLink>
        <BaseButton
          variant="ghost"
          size="sm"
          class="text-white hover:bg-white/10 lg:hidden"
          aria-label="Đóng menu"
          @click="mobileOpen = false"
          ><X class="size-5"
        /></BaseButton>
      </div>
      <div class="px-5 pb-3 pt-6">
        <p class="text-[0.68rem] font-bold uppercase tracking-[0.18em] text-[var(--color-gold)]">
          {{ roleLabel }}
        </p>
        <p class="mt-1 text-sm text-stone-400">Quản lý tập trung, thao tác rõ ràng</p>
      </div>
      <nav class="flex-1 space-y-1 px-3" aria-label="Điều hướng quản lý">
        <RouterLink
          v-for="item in props.navigation"
          :key="item.to"
          :to="item.to"
          class="flex min-h-11 items-center gap-3 whitespace-nowrap rounded-[var(--radius-sm)] px-3 text-sm font-semibold text-stone-300 transition-colors hover:bg-white/10 hover:text-white"
          :class="isActive(item.to) && 'bg-[var(--color-primary)] text-white'"
          @click="mobileOpen = false"
          ><component :is="navIcon(item.to)" class="size-4.5 shrink-0" aria-hidden="true" />{{
            item.label
          }}</RouterLink
        >
        <RouterLink
          to="/profile"
          class="flex min-h-11 items-center gap-3 whitespace-nowrap rounded-[var(--radius-sm)] px-3 text-sm font-semibold text-stone-300 transition-colors hover:bg-white/10 hover:text-white"
          :class="isActive('/profile') && 'bg-[var(--color-primary)] text-white'"
          @click="mobileOpen = false"
          ><UserRound class="size-4.5" aria-hidden="true" />Hồ sơ cá nhân</RouterLink
        >
      </nav>
      <div class="border-t border-white/10 p-3">
        <RouterLink
          to="/"
          class="flex min-h-11 items-center gap-3 rounded-[var(--radius-sm)] px-3 text-sm font-semibold text-stone-300 hover:bg-white/10 hover:text-white"
          ><House class="size-4.5" aria-hidden="true" />Xem website</RouterLink
        >
        <BaseButton
          variant="ghost"
          block
          class="mt-1 justify-start text-stone-300 hover:bg-white/10 hover:text-white"
          :loading="logoutLoading"
          @click="logout"
          ><LogOut class="size-4.5" aria-hidden="true" />Đăng xuất</BaseButton
        >
      </div>
    </aside>

    <div class="min-w-0">
      <header
        class="sticky top-0 z-20 flex h-[72px] items-center border-b border-[var(--color-border)] bg-[var(--color-surface)]/95 px-4 backdrop-blur sm:px-6 lg:px-8"
      >
        <div class="flex items-center gap-3">
          <BaseButton
            variant="ghost"
            size="sm"
            class="lg:hidden"
            aria-label="Mở menu quản lý"
            @click="mobileOpen = true"
            ><Menu class="size-5"
          /></BaseButton>
          <div>
            <p class="text-xs font-semibold text-[var(--color-text-muted)]">{{ props.eyebrow }}</p>
            <p class="font-semibold text-[var(--color-text)]">
              {{ user?.full_name || user?.email }}
            </p>
          </div>
        </div>
      </header>
      <div v-if="logoutError" class="px-4 pt-4 sm:px-6 lg:px-8">
        <AppAlert variant="error" title="Chưa thể thu hồi phiên">{{ logoutError }}</AppAlert>
      </div>
      <main id="management-content" class="mx-auto max-w-[1440px] p-4 sm:p-6 lg:p-8">
        <slot :user="user" />
      </main>
    </div>
  </div>
</template>
