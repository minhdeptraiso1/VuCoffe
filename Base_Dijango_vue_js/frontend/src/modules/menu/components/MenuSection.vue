<script setup lang="ts">
import type { MenuItem as Item } from "../types/menu.types";
import MenuItem from "./MenuItem.vue";
defineProps<{ title: string; description?: string; items: Item[] }>();
defineEmits<{ select: [item: Item] }>();
</script>
<template>
  <section>
    <header class="mb-5">
      <p class="text-xs font-bold uppercase tracking-[0.18em] text-[var(--color-accent)]">
        Thực đơn Kim Thành
      </p>
      <h2 class="mt-1 font-[var(--font-display)] text-2xl font-bold">{{ title }}</h2>
      <p v-if="description" class="mt-1 text-sm text-[var(--color-text-muted)]">
        {{ description }}
      </p>
    </header>
    <div>
      <MenuItem
        v-for="item in items"
        :key="item.id"
        :item="item"
        @select="$emit('select', $event)"
      />
    </div>
  </section>
</template>
