<script setup lang="ts">
interface Props {
  title: string;
  description?: string;
}
const props = withDefaults(defineProps<Props>(), { description: "" });
</script>

<template>
  <div
    class="rounded-[var(--radius-lg)] border border-dashed border-[var(--color-border)] px-5 py-10 text-center"
  >
    <div
      aria-hidden="true"
      class="mx-auto mb-3 flex size-12 items-center justify-center rounded-full bg-[var(--color-primary-soft)] text-xl text-[var(--color-primary)]"
    >
      ◇
    </div>
    <h3 class="font-semibold">{{ props.title }}</h3>
    <p
      v-if="props.description"
      class="mx-auto mt-1 max-w-md text-sm text-[var(--color-text-muted)]"
    >
      {{ props.description }}
    </p>
    <div v-if="$slots.action" class="mt-4"><slot name="action" /></div>
  </div>
</template>
