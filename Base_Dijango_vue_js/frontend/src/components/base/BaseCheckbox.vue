<script setup lang="ts">
import { Check } from "lucide-vue-next";
interface Props {
  modelValue: boolean;
  id: string;
  name: string;
  label: string;
  description?: string;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), { description: "", disabled: false });
const emit = defineEmits<{ "update:modelValue": [value: boolean] }>();
</script>

<template>
  <label
    :for="props.id"
    class="flex items-start gap-3 rounded-[var(--radius-sm)] text-sm transition-colors"
    :class="[
      props.disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer',
      props.modelValue && 'bg-[var(--color-primary-soft)]',
    ]"
  >
    <input
      :id="props.id"
      :name="props.name"
      type="checkbox"
      :checked="props.modelValue"
      :disabled="props.disabled"
      class="peer sr-only"
      @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
    />
    <span
      class="mt-0.5 flex size-5 shrink-0 items-center justify-center rounded border border-[var(--color-border)] bg-[var(--color-surface)] text-white peer-focus-visible:outline peer-focus-visible:outline-2 peer-focus-visible:outline-offset-2 peer-focus-visible:outline-[var(--color-focus)] peer-checked:border-[var(--color-primary)] peer-checked:bg-[var(--color-primary)]"
      ><Check v-if="props.modelValue" class="size-3.5" aria-hidden="true"
    /></span>
    <span>
      <span class="block font-semibold">{{ props.label }}</span>
      <span v-if="props.description" class="mt-0.5 block text-[var(--color-text-muted)]">
        {{ props.description }}
      </span>
    </span>
  </label>
</template>
