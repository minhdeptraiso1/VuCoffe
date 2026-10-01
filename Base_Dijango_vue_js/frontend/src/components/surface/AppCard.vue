<script setup lang="ts">
interface Props {
  title?: string;
  description?: string;
  padding?: "none" | "sm" | "md";
}

const props = withDefaults(defineProps<Props>(), { title: "", description: "", padding: "md" });
</script>

<template>
  <section
    class="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] shadow-[var(--shadow-surface)]"
    :class="{ 'p-4': props.padding === 'sm', 'p-5 sm:p-6': props.padding === 'md' }"
  >
    <header v-if="props.title || props.description || $slots.header" class="mb-4">
      <slot name="header">
        <h2 v-if="props.title" class="font-[var(--font-display)] text-xl font-bold">
          {{ props.title }}
        </h2>
        <p v-if="props.description" class="mt-1 text-sm text-[var(--color-text-muted)]">
          {{ props.description }}
        </p>
      </slot>
    </header>
    <slot />
    <footer v-if="$slots.footer" class="mt-5 border-t border-[var(--color-border)] pt-4">
      <slot name="footer" />
    </footer>
  </section>
</template>
