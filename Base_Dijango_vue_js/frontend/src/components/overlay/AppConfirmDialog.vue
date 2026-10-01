<script setup lang="ts">
import { useId } from "vue";

import BaseButton from "@/components/base/BaseButton.vue";

import AppModal from "./AppModal.vue";

interface Props {
  open: boolean;
  title: string;
  description?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  loading?: boolean;
  destructive?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  description: "",
  confirmLabel: "Xác nhận",
  cancelLabel: "Hủy",
  loading: false,
  destructive: false,
});
const emit = defineEmits<{ close: []; confirm: [] }>();
const formId = `confirm-${useId()}`;
</script>

<template>
  <AppModal
    :id="formId"
    :open="props.open"
    :title="props.title"
    :description="props.description"
    @close="emit('close')"
  >
    <form :id="formId" @submit.prevent="emit('confirm')">
      <slot>
        <p class="text-sm text-[var(--color-text-muted)]">
          Vui lòng kiểm tra thông tin trước khi tiếp tục.
        </p>
      </slot>
    </form>
    <template #footer>
      <BaseButton variant="ghost" :disabled="props.loading" @click="emit('close')">
        {{ props.cancelLabel }}
      </BaseButton>
      <BaseButton
        type="submit"
        :form="formId"
        :variant="props.destructive ? 'danger' : 'primary'"
        :loading="props.loading"
      >
        {{ props.confirmLabel }}
      </BaseButton>
    </template>
  </AppModal>
</template>
