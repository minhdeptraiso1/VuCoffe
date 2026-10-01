<script setup lang="ts">
interface Props {
  variant?: "neutral" | "success" | "warning" | "error" | "info";
}
const props = withDefaults(defineProps<Props>(), { variant: "neutral" });
const variants = {
  neutral: "bg-[var(--color-surface-subtle)] text-[var(--color-text)]",
  success: "bg-[var(--color-success-soft)] text-[var(--color-success)]",
  warning: "bg-[var(--color-warning-soft)] text-[var(--color-warning)]",
  error: "bg-[var(--color-error-soft)] text-[var(--color-error)]",
  info: "bg-[var(--color-info-soft)] text-[var(--color-info)]",
};
</script>

<template>
  <span
    class="inline-flex min-h-6 items-center rounded-[var(--radius-pill)] px-2.5 py-0.5 text-xs font-bold"
    :class="variants[props.variant]"
  >
    <slot />
  </span>
</template>
