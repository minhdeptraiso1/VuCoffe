<script setup lang="ts">
import { computed, ref } from "vue";

interface Props {
  id: string;
  label?: string;
  accept?: string;
  maxSizeMb?: number;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  label: "Chọn tệp",
  accept: ".xlsx",
  maxSizeMb: 5,
  disabled: false,
});
const emit = defineEmits<{ select: [file: File | null] }>();
const fileName = ref("");
const error = ref("");
const acceptedFormats = computed(() =>
  props.accept.includes("image/") ? "JPG, PNG hoặc WEBP" : props.accept,
);

function selectFile(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0] ?? null;
  error.value = "";
  if (file && file.size > props.maxSizeMb * 1024 * 1024) {
    error.value = `Tệp vượt quá ${String(props.maxSizeMb)} MB.`;
    fileName.value = "";
    input.value = "";
    emit("select", null);
    return;
  }
  fileName.value = file?.name ?? "";
  emit("select", file);
}
</script>

<template>
  <div>
    <label
      :for="props.id"
      class="flex min-h-32 items-center justify-center rounded-[var(--radius-lg)] border border-dashed border-[var(--color-border)] bg-[var(--color-surface)] px-5 py-6 text-center transition-colors"
      :class="
        props.disabled
          ? 'cursor-not-allowed opacity-60'
          : 'cursor-pointer hover:border-[var(--color-primary)] hover:bg-[var(--color-primary-soft)]'
      "
    >
      <span>
        <span class="block font-semibold text-[var(--color-primary)]">{{ props.label }}</span>
        <span class="mt-1 block text-sm text-[var(--color-text-muted)]">
          {{ fileName || `${acceptedFormats}, tối đa ${props.maxSizeMb} MB` }}
        </span>
      </span>
      <input
        :id="props.id"
        type="file"
        class="sr-only"
        :accept="props.accept"
        :disabled="props.disabled"
        :aria-describedby="error ? `${props.id}-error` : undefined"
        @change="selectFile"
      />
    </label>
    <p
      v-if="error"
      :id="`${props.id}-error`"
      role="alert"
      class="mt-2 text-sm text-[var(--color-error)]"
    >
      {{ error }}
    </p>
  </div>
</template>
