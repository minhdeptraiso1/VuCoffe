<script setup lang="ts">
import BaseCheckbox from "@/components/base/BaseCheckbox.vue";
import type { MenuTopping } from "../types/menu.types";
defineProps<{ topping: MenuTopping; selected: boolean }>();
defineEmits<{ change: [selected: boolean] }>();
const money = (value: string) => `+${new Intl.NumberFormat("vi-VN").format(Number(value))}đ`;
</script>
<template>
  <BaseCheckbox
    :id="`topping-${topping.id}`"
    :model-value="selected"
    :name="`topping-${topping.id}`"
    :label="topping.name"
    :description="money(topping.price)"
    class="border border-[var(--color-border)] p-3"
    @update:model-value="$emit('change', $event)"
  />
</template>
