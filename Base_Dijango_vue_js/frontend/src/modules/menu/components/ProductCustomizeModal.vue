<script setup lang="ts">
import { computed, ref, watch } from "vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseTextarea from "@/components/base/BaseTextarea.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import AppModal from "@/components/overlay/AppModal.vue";
import { toAppError } from "@/lib/http/errors";
import { validateCustomizationRequest } from "../api/menu.api";
import type { CustomizedOrderItem, MenuItem } from "../types/menu.types";
import MenuImage from "./MenuImage.vue";
import OptionGroup from "./OptionGroup.vue";
import ToppingOption from "./ToppingOption.vue";
const props = defineProps<{ modelValue: boolean; item: MenuItem | null }>();
const emit = defineEmits<{
  "update:modelValue": [value: boolean];
  addToCart: [item: CustomizedOrderItem];
}>();
const variantId = ref(0);
const sweetness = ref("");
const ice = ref("");
const toppingIds = ref<number[]>([]);
const note = ref("");
const quantity = ref(1);
const loading = ref(false);
const error = ref("");
watch(
  () => props.item,
  (item) => {
    variantId.value = item?.variants.find((v) => v.is_default)?.id ?? item?.variants[0]?.id ?? 0;
    sweetness.value = item?.sweetness_options[0] ?? "";
    ice.value = item?.ice_options[0] ?? "";
    toppingIds.value = [];
    note.value = "";
    quantity.value = 1;
    error.value = "";
  },
  { immediate: true },
);
const variantOptions = computed(
  () =>
    props.item?.variants.map((v) => ({
      value: String(v.id),
      label: `${v.name}${v.volume_ml ? ` · ${String(v.volume_ml)}ml` : ""} · ${money(v.price)}`,
    })) ?? [],
);
const sweetnessOptions = computed(
  () => props.item?.sweetness_options.map((value) => ({ value, label: value })) ?? [],
);
const iceOptions = computed(
  () => props.item?.ice_options.map((value) => ({ value, label: value })) ?? [],
);
const estimate = computed(() => {
  const variant = props.item?.variants.find((v) => v.id === variantId.value);
  const toppings =
    props.item?.toppings
      .filter((t) => toppingIds.value.includes(t.id))
      .reduce((sum, t) => sum + Number(t.price), 0) ?? 0;
  return (Number(variant?.price ?? 0) + toppings) * quantity.value;
});
function money(value: string | number) {
  return new Intl.NumberFormat("vi-VN").format(Number(value)) + "đ";
}
function toggleTopping(id: number, selected: boolean) {
  toppingIds.value = selected
    ? [...toppingIds.value, id]
    : toppingIds.value.filter((value) => value !== id);
}
function close() {
  emit("update:modelValue", false);
}
async function confirm() {
  if (!props.item || !variantId.value) return;
  loading.value = true;
  error.value = "";
  try {
    const result = await validateCustomizationRequest(props.item.slug, {
      variant_id: variantId.value,
      topping_ids: toppingIds.value,
      sweetness: sweetness.value,
      ice: ice.value,
      quantity: quantity.value,
    });
    const variant = props.item.variants.find((v) => v.id === variantId.value);
    emit("addToCart", {
      item: props.item,
      size: variant?.name ?? "Mặc định",
      sweetness: sweetness.value,
      ice: ice.value,
      toppings: props.item.toppings
        .filter((t) => toppingIds.value.includes(t.id))
        .map((t) => t.name),
      note: note.value.trim(),
      quantity: quantity.value,
      finalPrice: Number(result.total_price),
    });
    close();
  } catch (reason) {
    error.value = toAppError(reason).message;
  } finally {
    loading.value = false;
  }
}
</script>
<template>
  <AppModal
    id="product-customize"
    :open="modelValue && Boolean(item)"
    title="Tùy chỉnh món"
    description="Chọn khẩu vị, món thêm và số lượng."
    size="lg"
    sticky-footer
    @close="close"
    ><template v-if="item"
      ><div class="grid gap-6 md:grid-cols-[240px_1fr]">
        <div>
          <MenuImage
            :src="item.image_url"
            :alt="item.name"
            :position="item.image_position"
            class="rounded-[var(--radius-md)]"
          />
          <h3 class="mt-3 text-lg font-bold">{{ item.name }}</h3>
          <p class="mt-3 text-sm leading-5 text-[var(--color-text-muted)]">
            {{ item.description }}
          </p>
        </div>
        <div class="space-y-5">
          <OptionGroup
            v-if="variantOptions.length"
            legend="Kích cỡ"
            :model-value="String(variantId)"
            :options="variantOptions"
            @update:model-value="variantId = Number($event)"
          /><OptionGroup
            v-if="sweetnessOptions.length"
            v-model="sweetness"
            legend="Độ ngọt"
            :options="sweetnessOptions"
          /><OptionGroup
            v-if="iceOptions.length"
            v-model="ice"
            legend="Lượng đá / nhiệt độ"
            :options="iceOptions"
          />
          <fieldset v-if="item.toppings.length">
            <legend class="text-sm font-bold">Món thêm</legend>
            <div class="mt-2 grid gap-2 sm:grid-cols-2">
              <ToppingOption
                v-for="topping in item.toppings"
                :key="topping.id"
                :topping="topping"
                :selected="toppingIds.includes(topping.id)"
                @change="toggleTopping(topping.id, $event)"
              />
            </div>
          </fieldset>
          <div>
            <label for="custom-note" class="text-sm font-bold">Ghi chú cho barista</label
            ><BaseTextarea
              id="custom-note"
              v-model="note"
              name="custom-note"
              class="mt-2"
              :rows="2"
              placeholder="Ví dụ: mang đi, làm ấm nhẹ…"
            />
          </div>
          <AppAlert v-if="error" variant="error" title="Chưa thể thêm món">{{ error }}</AppAlert>
        </div>
      </div></template
    ><template #footer
      ><div class="flex w-full flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <BaseButton
            size="sm"
            variant="secondary"
            :disabled="quantity <= 1"
            aria-label="Giảm số lượng"
            @click="quantity--"
            >−</BaseButton
          ><output class="min-w-8 text-center font-bold">{{ quantity }}</output
          ><BaseButton size="sm" variant="secondary" aria-label="Tăng số lượng" @click="quantity++"
            >+</BaseButton
          >
        </div>
        <div class="flex items-center gap-4">
          <div class="text-right">
            <span class="block text-xs text-[var(--color-text-muted)]">Tạm tính</span
            ><strong class="text-[var(--color-primary)]">{{ money(estimate) }}</strong>
          </div>
          <BaseButton :loading="loading" @click="confirm">Thêm vào giỏ</BaseButton>
        </div>
      </div></template
    ></AppModal
  >
</template>
