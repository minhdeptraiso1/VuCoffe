<script setup lang="ts">
import { storeToRefs } from "pinia";

import { useToastStore } from "@/app/stores/toast";

const toast = useToastStore();
const { message, variant } = storeToRefs(toast);
const styles = {
  success:
    "border-[var(--color-success)] bg-[var(--color-success-soft)] text-[var(--color-success)]",
  error: "border-[var(--color-error)] bg-[var(--color-error-soft)] text-[var(--color-error)]",
  info: "border-[var(--color-info)] bg-[var(--color-info-soft)] text-[var(--color-info)]",
};
</script>

<template>
  <Transition name="toast">
    <div
      v-if="message"
      class="fixed right-4 top-4 z-[var(--z-toast)] max-w-[calc(100vw-2rem)] cursor-pointer rounded-[var(--radius-md)] border px-4 py-3 text-left shadow-[var(--shadow-overlay)] transition hover:brightness-95 focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-[var(--color-focus)] sm:max-w-md"
      :class="styles[variant]"
      :role="variant === 'error' ? 'alert' : 'status'"
      :aria-live="variant === 'error' ? 'assertive' : 'polite'"
      :aria-label="`${message}. Nhấn để đóng thông báo.`"
      tabindex="0"
      @click="toast.dismiss"
      @keydown.enter="toast.dismiss"
      @keydown.space.prevent="toast.dismiss"
    >
      <p class="text-sm font-medium">{{ message }}</p>
      <span class="mt-1 block text-xs opacity-75">Nhấn để đóng</span>
    </div>
  </Transition>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition:
    opacity 180ms ease,
    transform 180ms ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
