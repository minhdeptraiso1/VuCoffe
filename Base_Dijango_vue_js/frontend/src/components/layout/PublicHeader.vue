<script setup lang="ts">
import { computed, ref } from "vue";
import { LogOut, Menu, ShoppingBag, UserRound, X } from "lucide-vue-next";
import { useRoute } from "vue-router";

import BaseButton from "@/components/base/BaseButton.vue";
import AppLogo from "@/components/brand/AppLogo.vue";
import { roleHomePath, useAuth } from "@/modules/auth/composables/useAuth";

interface Props {
  cartCount?: number;
}
const props = withDefaults(defineProps<Props>(), { cartCount: undefined });
const emit = defineEmits<{ openCart: [] }>();
const route = useRoute();
const mobileOpen = ref(false);
const { user, isAuthenticated, logout, logoutLoading } = useAuth();
const accountPath = computed(() => (user.value ? roleHomePath(user.value.role) : "/login"));
const navigation = [
  { label: "Trang chủ", to: "/" },
  { label: "Thực đơn", to: "/menu" },
  { label: "Về Kim Thành", to: "/#coffee-heaven" },
  { label: "Không gian quán", to: "/#ambiance" },
  { label: "Quy trình rang mộc", to: "/#process" },
];
function isActive(to: string) {
  return to === "/menu" ? route.path === "/menu" : to === "/" ? route.path === "/" : false;
}
</script>

<template>
  <header
    class="sticky top-0 z-[var(--z-sticky)] border-b border-white/10 bg-[var(--color-espresso-dark)]/95 text-white backdrop-blur-md"
  >
    <div class="mx-auto flex h-[71px] max-w-7xl items-center gap-5 px-4 sm:px-6 lg:px-8">
      <RouterLink to="/" class="shrink-0" aria-label="Kim Thành Coffee - Trang chủ"
        ><AppLogo variant="pill" size="md"
      /></RouterLink>
      <nav
        class="hidden min-w-0 flex-1 items-center justify-center gap-5 lg:flex"
        aria-label="Điều hướng chính"
      >
        <RouterLink
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="whitespace-nowrap border-b-2 border-transparent px-1 py-2 text-sm font-semibold text-stone-300 transition-colors hover:text-white"
          :class="isActive(item.to) && 'border-[var(--color-gold)] text-white'"
          >{{ item.label }}</RouterLink
        >
      </nav>
      <div class="ml-auto hidden shrink-0 items-center gap-2 lg:flex">
        <BaseButton
          v-if="props.cartCount !== undefined"
          size="sm"
          variant="secondary"
          class="whitespace-nowrap border-white/20 bg-white/10 text-white hover:bg-white/20"
          @click="emit('openCart')"
          ><ShoppingBag class="size-4 text-[var(--color-gold)]" aria-hidden="true" />Giỏ hàng<span
            v-if="props.cartCount"
            class="rounded-full bg-[var(--color-gold)] px-1.5 text-xs text-[var(--color-espresso-dark)]"
            >{{ props.cartCount }}</span
          ></BaseButton
        >
        <template v-if="isAuthenticated && user">
          <RouterLink
            :to="accountPath"
            class="inline-flex min-h-10 max-w-44 items-center gap-2 whitespace-nowrap rounded-[var(--radius-pill)] border border-white/20 px-3 text-sm font-semibold hover:bg-white/10"
            ><UserRound class="size-4 text-[var(--color-gold)]" aria-hidden="true" /><span
              class="truncate"
              >{{ user.full_name || user.email }}</span
            ></RouterLink
          >
          <BaseButton
            size="sm"
            variant="ghost"
            class="whitespace-nowrap text-stone-200 hover:bg-white/10 hover:text-white"
            :loading="logoutLoading"
            @click="logout"
            ><LogOut class="size-4" aria-hidden="true" />Đăng xuất</BaseButton
          >
        </template>
        <template v-else>
          <RouterLink
            to="/login"
            class="whitespace-nowrap px-3 text-sm font-semibold text-stone-200 hover:text-white"
            >Đăng nhập</RouterLink
          >
          <RouterLink
            to="/register"
            class="inline-flex min-h-10 items-center whitespace-nowrap rounded-[var(--radius-pill)] bg-[var(--color-gold)] px-4 text-sm font-bold text-[var(--color-espresso-dark)] hover:brightness-110"
            >Đăng ký</RouterLink
          >
        </template>
      </div>
      <BaseButton
        variant="ghost"
        size="sm"
        class="ml-auto text-white hover:bg-white/10 lg:hidden"
        :aria-label="mobileOpen ? 'Đóng menu' : 'Mở menu'"
        :aria-expanded="mobileOpen"
        @click="mobileOpen = !mobileOpen"
        ><X v-if="mobileOpen" class="size-5" /><Menu v-else class="size-5"
      /></BaseButton>
    </div>
    <div v-if="mobileOpen" class="border-t border-white/10 px-4 py-4 lg:hidden">
      <nav class="mx-auto grid max-w-7xl gap-1" aria-label="Điều hướng di động">
        <RouterLink
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="min-h-11 rounded-[var(--radius-sm)] px-3 py-2.5 text-sm font-semibold text-stone-200 hover:bg-white/10"
          @click="mobileOpen = false"
          >{{ item.label }}</RouterLink
        >
        <RouterLink
          :to="accountPath"
          class="min-h-11 rounded-[var(--radius-sm)] px-3 py-2.5 text-sm font-semibold text-stone-200 hover:bg-white/10"
          @click="mobileOpen = false"
          >{{ isAuthenticated ? "Tài khoản của tôi" : "Đăng nhập" }}</RouterLink
        >
        <BaseButton
          v-if="isAuthenticated"
          variant="ghost"
          block
          class="justify-start text-stone-200 hover:bg-white/10"
          :loading="logoutLoading"
          @click="logout"
          >Đăng xuất</BaseButton
        >
      </nav>
    </div>
  </header>
</template>
