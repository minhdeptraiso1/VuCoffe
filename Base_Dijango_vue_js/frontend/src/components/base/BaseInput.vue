<script setup lang="ts">
import { computed, ref, useAttrs } from "vue";

defineOptions({ inheritAttrs: false });

interface Props {
  modelValue: string;
  id: string;
  name: string;
  type?: "text" | "email" | "password" | "number";
  autocomplete?: string;
  placeholder?: string;
  disabled?: boolean;
  readonly?: boolean;
  required?: boolean;
  invalid?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  type: "text",
  autocomplete: "off",
  placeholder: "",
  disabled: false,
  readonly: false,
  required: false,
  invalid: false,
});
const emit = defineEmits<{ "update:modelValue": [value: string]; blur: [event: FocusEvent] }>();
const attrs = useAttrs();
const passwordVisible = ref(false);
const actualType = computed(() =>
  props.type === "password" && passwordVisible.value ? "text" : props.type,
);
</script>

<template>
  <div class="relative">
    <input
      v-bind="attrs"
      :id="props.id"
      :name="props.name"
      :value="props.modelValue"
      :type="actualType"
      :autocomplete="props.autocomplete"
      :placeholder="props.placeholder"
      :disabled="props.disabled"
      :readonly="props.readonly"
      :required="props.required"
      :aria-invalid="props.invalid || undefined"
      class="min-h-11 w-full rounded-[var(--radius-sm)] border bg-[var(--color-surface)] px-3 text-base text-[var(--color-text)] shadow-sm transition-colors placeholder:text-[var(--color-text-muted)] disabled:cursor-not-allowed disabled:bg-[var(--color-surface-subtle)] disabled:text-[var(--color-text-muted)] sm:text-sm"
      :class="[
        props.invalid
          ? 'border-[var(--color-error)]'
          : 'border-[var(--color-border)] hover:border-[var(--color-primary)]',
        props.type === 'password' && 'pr-16',
      ]"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      @blur="emit('blur', $event)"
    />
    <button
      v-if="props.type === 'password'"
      type="button"
      class="absolute inset-y-0 right-1 min-w-12 cursor-pointer rounded-md px-2 text-sm font-semibold text-[var(--color-primary)] hover:bg-[var(--color-primary-soft)]"
      :aria-label="passwordVisible ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'"
      @click="passwordVisible = !passwordVisible"
    >
      {{ passwordVisible ? "Ẩn" : "Hiện" }}
    </button>
  </div>
</template>
