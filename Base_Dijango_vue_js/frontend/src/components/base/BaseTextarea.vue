<script setup lang="ts">
defineOptions({ inheritAttrs: false });

interface Props {
  modelValue: string;
  id: string;
  name: string;
  rows?: number;
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  invalid?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  rows: 4,
  placeholder: "",
  disabled: false,
  required: false,
  invalid: false,
});
const emit = defineEmits<{ "update:modelValue": [value: string]; blur: [event: FocusEvent] }>();
</script>

<template>
  <textarea
    v-bind="$attrs"
    :id="props.id"
    :name="props.name"
    :value="props.modelValue"
    :rows="props.rows"
    :placeholder="props.placeholder"
    :disabled="props.disabled"
    :required="props.required"
    :aria-invalid="props.invalid || undefined"
    class="w-full resize-y rounded-[var(--radius-sm)] border bg-[var(--color-surface)] px-3 py-2 text-base text-[var(--color-text)] shadow-sm placeholder:text-[var(--color-text-muted)] disabled:cursor-not-allowed disabled:bg-[var(--color-surface-subtle)] sm:text-sm"
    :class="
      props.invalid
        ? 'border-[var(--color-error)]'
        : 'border-[var(--color-border)] hover:border-[var(--color-primary)]'
    "
    @input="emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    @blur="emit('blur', $event)"
  />
</template>
