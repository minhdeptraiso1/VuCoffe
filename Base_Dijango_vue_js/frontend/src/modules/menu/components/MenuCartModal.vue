<script setup lang="ts">
import { Trash2 } from "lucide-vue-next";
import BaseButton from "@/components/base/BaseButton.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import AppEmptyState from "@/components/feedback/AppEmptyState.vue";
import AppDrawer from "@/components/overlay/AppDrawer.vue";
import type { CartItem } from "../types/menu.types";
import MenuImage from "./MenuImage.vue";

defineProps<{ open: boolean; items: CartItem[]; subtotal: number }>();
const emit = defineEmits<{ close: []; remove: [id: string] }>();
function formatVnd(amount: number) {
  return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(amount);
}
</script>

<template>
  <AppDrawer
    id="menu-cart"
    :open="open"
    title="Giỏ hàng của bạn"
    description="Kiểm tra món và tùy chọn trước khi đặt."
    @close="emit('close')"
  >
    <AppEmptyState
      v-if="items.length === 0"
      title="Giỏ hàng đang trống"
      description="Chọn một món trong thực đơn để bắt đầu."
    >
      <template #action><BaseButton @click="emit('close')">Xem thực đơn</BaseButton></template>
    </AppEmptyState>
    <ul v-else class="space-y-3" aria-label="Các món trong giỏ hàng">
      <li
        v-for="cartItem in items"
        :key="cartItem.id"
        class="flex gap-3 rounded-[var(--radius-md)] border border-[var(--color-border)] p-3"
      >
        <MenuImage
          :src="cartItem.item.image_url"
          :alt="cartItem.item.name"
          :position="cartItem.item.image_position"
          class="h-20 w-20 shrink-0 rounded-[var(--radius-sm)]"
        />
        <div class="min-w-0 flex-1">
          <div class="flex items-start justify-between gap-2">
            <div>
              <h3 class="font-semibold">{{ cartItem.item.name }}</h3>
              <p class="mt-0.5 text-xs text-[var(--color-text-muted)]">
                Size {{ cartItem.size }} · {{ cartItem.sweetness }} · {{ cartItem.ice }}
              </p>
            </div>
            <BaseButton
              variant="ghost"
              size="sm"
              :aria-label="`Xóa ${cartItem.item.name}`"
              @click="emit('remove', cartItem.id)"
              ><Trash2 class="size-4" aria-hidden="true"
            /></BaseButton>
          </div>
          <p v-if="cartItem.toppings.length" class="mt-1 text-xs text-[var(--color-accent)]">
            Topping: {{ cartItem.toppings.join(", ") }}
          </p>
          <p v-if="cartItem.note" class="mt-1 text-xs italic text-[var(--color-text-muted)]">
            “{{ cartItem.note }}”
          </p>
          <div class="mt-2 flex items-center justify-between text-sm">
            <span>Số lượng: {{ cartItem.quantity }}</span
            ><strong class="text-[var(--color-primary)]">{{
              formatVnd(cartItem.finalPrice)
            }}</strong>
          </div>
        </div>
      </li>
    </ul>
    <template v-if="items.length" #footer>
      <div class="flex items-center justify-between">
        <span class="text-sm text-[var(--color-text-muted)]">Tạm tính</span
        ><strong class="text-xl text-[var(--color-primary)]">{{ formatVnd(subtotal) }}</strong>
      </div>
      <AppAlert class="mt-4" variant="info" title="Đặt hàng trực tuyến sắp mở"
        >Bước xác nhận đơn sẽ được bật khi API đơn hàng hoàn tất.</AppAlert
      >
      <BaseButton class="mt-4" block @click="emit('close')">Tiếp tục chọn món</BaseButton>
    </template>
  </AppDrawer>
</template>
