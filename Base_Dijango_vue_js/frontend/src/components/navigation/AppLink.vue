<script setup lang="ts">
import { RouterLink, type RouteLocationRaw } from "vue-router";

const props = withDefaults(
  defineProps<{ to: RouteLocationRaw; variant?: "default" | "nav" | "button" }>(),
  { variant: "default" },
);

const variants = {
  default:
    "font-semibold text-[var(--color-primary)] underline-offset-4 hover:text-[var(--color-primary-hover)] hover:underline",
  nav: "font-semibold text-[var(--color-text)] hover:text-[var(--color-primary)]",
  button:
    "min-h-11 bg-[var(--color-primary)] px-5 py-2.5 font-semibold text-white shadow-sm hover:bg-[var(--color-primary-hover)]",
};
</script>

<template>
  <RouterLink
    :to="to"
    class="inline-flex cursor-pointer items-center justify-center rounded-[var(--radius-sm)] transition-colors"
    :class="variants[props.variant]"
  >
    <slot />
  </RouterLink>
</template>
