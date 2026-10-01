<script setup lang="ts">
import { Plus, Star } from "lucide-vue-next";

import DrinkIllustration from "@/components/brand/DrinkIllustration.vue";
import type { MenuItem } from "../data/menuData";

defineProps<{ item: MenuItem }>();
const emit = defineEmits<{ select: [item: MenuItem] }>();
</script>

<template>
  <article
    class="group flex h-full flex-col overflow-hidden rounded-3xl border border-[#e2d4c0] bg-white shadow-xs transition-all duration-300 hover:-translate-y-1.5 hover:border-[#6f3f25] hover:shadow-2xl"
  >
    <div class="relative overflow-hidden bg-stone-50 p-3">
      <DrinkIllustration
        :type="item.illustrationType"
        :image="item.image"
        :alt="item.name"
        size="md"
        class="w-full rounded-2xl transition-transform duration-500 group-hover:scale-105"
      />
      <div class="absolute left-5 top-5 flex flex-wrap gap-2">
        <span
          v-if="item.isBestSeller"
          class="rounded-full bg-[#b85c38] px-3 py-1 text-[0.65rem] font-bold uppercase tracking-wider text-white shadow-sm"
        >
          Bán chạy
        </span>
        <span
          v-if="item.isNew"
          class="rounded-full bg-[#dfab71] px-3 py-1 text-[0.65rem] font-bold uppercase tracking-wider text-[#160e08] shadow-sm"
        >
          Món mới
        </span>
      </div>
    </div>

    <div class="flex flex-1 flex-col p-5 sm:p-6">
      <div class="flex items-start justify-between gap-3">
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-[#b85c38]">
            {{ item.tag }}
          </p>
          <h2
            class="mt-1 font-[var(--font-display)] text-xl font-bold leading-tight text-[#1c130d] group-hover:text-[#6f3f25] transition-colors"
          >
            {{ item.name }}
          </h2>
        </div>
        <p class="shrink-0 font-[var(--font-display)] text-lg font-bold text-[#6f3f25]">
          {{ item.formattedPrice }}
        </p>
      </div>

      <div class="mt-2.5 flex flex-wrap items-center gap-x-2.5 gap-y-1 text-xs text-[#6f6256]">
        <span
          v-if="item.volume"
          class="rounded-md bg-stone-100 px-2 py-0.5 font-medium text-stone-600"
        >
          {{ item.volume }}
        </span>
        <span
          v-if="item.calories"
          class="rounded-md bg-stone-100 px-2 py-0.5 font-medium text-stone-600"
        >
          {{ item.calories }} kcal
        </span>
        <span class="inline-flex items-center gap-1 font-semibold text-[#1c130d]">
          <Star class="size-3.5 fill-[#c58940] text-[#c58940]" aria-hidden="true" />
          {{ item.rating }}
          <span class="font-normal text-[#6f6256]">({{ item.reviewCount }})</span>
        </span>
      </div>

      <p class="mt-3 line-clamp-2 text-xs sm:text-sm leading-relaxed text-[#6f6256] font-light">
        {{ item.description }}
      </p>

      <div
        class="mt-auto flex items-center justify-between gap-3 border-t border-[#e2d4c0]/80 pt-4"
      >
        <div class="min-w-0 text-xs text-[#6f6256]">
          <span class="block text-[0.7rem]">Giá từ</span>
          <strong class="font-[var(--font-display)] text-lg font-bold text-[#1c130d]">
            {{ item.formattedPrice }}
          </strong>
        </div>
        <button
          type="button"
          class="inline-flex items-center gap-1.5 rounded-full bg-[#1c130d] px-4 py-2 text-xs font-bold text-white shadow-sm transition-all duration-200 hover:bg-[#6f3f25] hover:scale-103 cursor-pointer"
          :aria-label="`Tùy chỉnh ${item.name}`"
          @click="emit('select', item)"
        >
          <Plus class="size-3.5" aria-hidden="true" />
          <span>Tùy chỉnh</span>
        </button>
      </div>
    </div>
  </article>
</template>
