<script setup lang="ts">
interface Props {
  variant?: "info" | "success" | "warning" | "error";
  title?: string;
}

const props = withDefaults(defineProps<Props>(), { variant: "info", title: "" });
const styles = {
  info: "border-[var(--color-info)] bg-[var(--color-info-soft)] text-[var(--color-info)]",
  success:
    "border-[var(--color-success)] bg-[var(--color-success-soft)] text-[var(--color-success)]",
  warning:
    "border-[var(--color-warning)] bg-[var(--color-warning-soft)] text-[var(--color-warning)]",
  error: "border-[var(--color-error)] bg-[var(--color-error-soft)] text-[var(--color-error)]",
};
</script>

<template>
  <div
    class="rounded-[var(--radius-sm)] border p-3 text-sm"
    :class="styles[props.variant]"
    :role="props.variant === 'error' ? 'alert' : 'status'"
  >
    <p v-if="props.title" class="font-semibold">{{ props.title }}</p>
    <div :class="props.title && 'mt-1'"><slot /></div>
  </div>
</template>
