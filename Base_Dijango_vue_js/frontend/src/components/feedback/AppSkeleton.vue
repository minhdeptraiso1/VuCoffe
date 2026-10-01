<script setup lang="ts">
interface Props {
  lines?: number;
}
const props = withDefaults(defineProps<Props>(), { lines: 3 });
</script>

<template>
  <div role="status" aria-label="Đang tải" class="space-y-3">
    <span
      v-for="line in props.lines"
      :key="line"
      class="block h-4 animate-pulse rounded bg-[var(--color-surface-subtle)]"
      :class="line === props.lines ? 'w-2/3' : 'w-full'"
    />
    <span class="sr-only">Đang tải nội dung</span>
  </div>
</template>
