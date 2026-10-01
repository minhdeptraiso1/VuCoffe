<script setup lang="ts">
import BaseButton from "@/components/base/BaseButton.vue";
import { menuPrice } from "../composables/useMenuCatalog";
import type { MenuItem } from "../types/menu.types";
import MenuImage from "./MenuImage.vue";
defineProps<{ item: MenuItem }>();
defineEmits<{ select: [item: MenuItem] }>();
const money = (value: number) => new Intl.NumberFormat("vi-VN").format(value) + "đ";
</script>
<template>
  <article
    class="group grid grid-cols-[96px_minmax(0,1fr)] gap-4 border-b border-[var(--color-border)] py-4 sm:grid-cols-[120px_minmax(0,1fr)]"
  >
    <MenuImage
      :src="item.image_url"
      :alt="item.name"
      :position="item.image_position"
      class="w-full self-start rounded-[var(--radius-sm)]"
    />
    <div class="min-w-0">
      <div class="flex items-baseline gap-2">
        <h3 class="min-w-0 font-semibold group-hover:text-[var(--color-primary)]">
          {{ item.name }}
        </h3>
        <span class="min-w-3 flex-1 border-b border-dotted border-[var(--color-border)]"></span>
        <strong class="shrink-0 whitespace-nowrap text-sm text-[var(--color-primary)]">
          {{ money(menuPrice(item)) }}
        </strong>
      </div>
      <p class="mt-1 line-clamp-2 text-sm leading-5 text-[var(--color-text-muted)]">
        {{ item.description }}
      </p>
      <BaseButton
        variant="text"
        size="sm"
        class="mt-1 !min-h-8 !px-0"
        :aria-label="`Tùy chỉnh ${item.name}`"
        @click="$emit('select', item)"
        >Tùy chỉnh món →</BaseButton
      >
    </div>
  </article>
</template>
