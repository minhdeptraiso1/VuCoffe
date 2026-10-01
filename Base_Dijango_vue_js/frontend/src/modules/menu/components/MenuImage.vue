<script setup lang="ts">
import { ref } from "vue";
defineProps<{ src: string; alt: string; position?: string }>();
const failed = ref(false);
</script>
<template>
  <div class="aspect-[4/3] overflow-hidden bg-[var(--color-primary-soft)]">
    <img
      v-if="src && !failed"
      :src="src"
      :alt="alt"
      class="h-full w-full object-cover transition duration-500 hover:scale-[1.02]"
      :style="{ objectPosition: position || 'center center' }"
      loading="lazy"
      @error="failed = true"
    />
    <div
      v-else
      class="flex h-full items-center justify-center px-6 text-center text-sm text-[var(--color-text-muted)]"
    >
      Ảnh món đang được cập nhật
    </div>
  </div>
</template>
