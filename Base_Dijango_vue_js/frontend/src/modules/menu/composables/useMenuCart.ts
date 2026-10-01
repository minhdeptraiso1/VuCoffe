import { computed, ref } from "vue";

import type { CartItem, CustomizedOrderItem } from "../types/menu.types";

export function useMenuCart() {
  const items = ref<CartItem[]>([]);

  const totalItems = computed(() =>
    items.value.reduce((total, cartItem) => total + cartItem.quantity, 0),
  );
  const subtotal = computed(() =>
    items.value.reduce((total, cartItem) => total + cartItem.finalPrice, 0),
  );

  function addItem(orderItem: CustomizedOrderItem) {
    items.value.push({
      ...orderItem,
      id: `${String(orderItem.item.id)}-${globalThis.crypto.randomUUID()}`,
    });
  }

  function removeItem(id: string) {
    items.value = items.value.filter((item) => item.id !== id);
  }

  return { items, totalItems, subtotal, addItem, removeItem };
}
