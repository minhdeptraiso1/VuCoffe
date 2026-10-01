<script setup lang="ts">
import AppAlert from "@/components/feedback/AppAlert.vue";
import PublicHeader from "@/components/layout/PublicHeader.vue";
import { useAuthStore } from "@/modules/auth/stores/auth";
import { storeToRefs } from "pinia";

const auth = useAuthStore();
const { user, logoutError } = storeToRefs(auth);
</script>

<template>
  <div class="min-h-screen bg-[var(--color-background)]">
    <PublicHeader />

    <div v-if="logoutError" class="mx-auto max-w-6xl px-4 pt-4 sm:px-6 lg:px-8">
      <AppAlert variant="error" title="Chưa thể thu hồi phiên trên máy chủ">
        {{ logoutError }} Bạn có thể thử đăng xuất lại khi có mạng.
      </AppAlert>
    </div>

    <main class="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
      <slot :user="user" />
    </main>
  </div>
</template>
