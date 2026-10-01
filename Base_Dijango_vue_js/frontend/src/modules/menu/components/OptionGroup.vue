<script setup lang="ts">
import BaseButton from "@/components/base/BaseButton.vue";
defineProps<{
  legend: string;
  modelValue: string;
  options: Array<{ value: string; label: string }>;
}>();
defineEmits<{ "update:modelValue": [value: string] }>();
</script>
<template>
  <fieldset>
    <legend class="text-sm font-bold">{{ legend }}</legend>
    <div class="mt-2 flex flex-wrap gap-2">
      <BaseButton
        v-for="option in options"
        :key="option.value"
        size="sm"
        :variant="modelValue === option.value ? 'primary' : 'secondary'"
        :aria-pressed="modelValue === option.value"
        @click="$emit('update:modelValue', option.value)"
        >{{ option.label }}</BaseButton
      >
    </div>
  </fieldset>
</template>
