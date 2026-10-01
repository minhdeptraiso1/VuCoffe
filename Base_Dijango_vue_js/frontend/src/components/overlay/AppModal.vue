<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref, watch } from "vue";

interface Props {
  open: boolean;
  title: string;
  description?: string;
  closeLabel?: string;
  size?: "sm" | "md" | "lg";
  stickyFooter?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  description: "",
  closeLabel: "Đóng hộp thoại",
  size: "md",
  stickyFooter: false,
});
const emit = defineEmits<{ close: [] }>();
const dialog = ref<HTMLElement | null>(null);
let previousFocus: HTMLElement | null = null;

function focusableElements() {
  return Array.from(
    dialog.value?.querySelectorAll<HTMLElement>(
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
    ) ?? [],
  );
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === "Escape") {
    emit("close");
    return;
  }
  if (event.key !== "Tab") return;
  const items = focusableElements();
  if (items.length === 0) return;
  const first = items[0];
  const last = items.at(-1);
  if (event.shiftKey && globalThis.document.activeElement === first) {
    event.preventDefault();
    last?.focus();
  } else if (!event.shiftKey && globalThis.document.activeElement === last) {
    event.preventDefault();
    first?.focus();
  }
}

watch(
  () => props.open,
  async (open) => {
    if (open) {
      previousFocus = globalThis.document.activeElement as HTMLElement | null;
      globalThis.document.body.style.overflow = "hidden";
      await nextTick();
      focusableElements()[0]?.focus();
    } else {
      globalThis.document.body.style.overflow = "";
      previousFocus?.focus();
    }
  },
);

onBeforeUnmount(() => {
  globalThis.document.body.style.overflow = "";
});
</script>

<template>
  <Teleport to="body">
    <div
      v-if="props.open"
      class="fixed inset-0 z-[var(--z-overlay)] flex items-end justify-center bg-[var(--color-overlay)] p-0 sm:items-center sm:p-5"
      @mousedown.self="emit('close')"
    >
      <section
        ref="dialog"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="`${$attrs.id ?? 'app-modal'}-title`"
        :aria-describedby="
          props.description ? `${$attrs.id ?? 'app-modal'}-description` : undefined
        "
        class="max-h-[92vh] w-full overflow-y-auto rounded-t-[var(--radius-lg)] bg-[var(--color-surface)] p-5 shadow-[var(--shadow-overlay)] sm:rounded-[var(--radius-lg)] sm:p-6"
        :class="
          props.size === 'lg' ? 'sm:max-w-3xl' : props.size === 'sm' ? 'sm:max-w-md' : 'sm:max-w-lg'
        "
        @keydown="onKeydown"
      >
        <header class="flex items-start justify-between gap-4">
          <div>
            <h2
              :id="`${$attrs.id ?? 'app-modal'}-title`"
              class="font-[var(--font-display)] text-2xl font-bold"
            >
              {{ props.title }}
            </h2>
            <p
              v-if="props.description"
              :id="`${$attrs.id ?? 'app-modal'}-description`"
              class="mt-1 text-sm text-[var(--color-text-muted)]"
            >
              {{ props.description }}
            </p>
          </div>
          <button
            type="button"
            class="flex size-10 shrink-0 items-center justify-center rounded-full text-xl hover:bg-[var(--color-primary-soft)]"
            :aria-label="props.closeLabel"
            @click="emit('close')"
          >
            <span aria-hidden="true">×</span>
          </button>
        </header>
        <div class="mt-5"><slot /></div>
        <footer
          v-if="$slots.footer"
          class="mt-6 flex flex-wrap justify-end gap-3"
          :class="
            props.stickyFooter &&
            'sticky -bottom-5 -mx-5 border-t border-[var(--color-border)] bg-[var(--color-surface)] p-5 sm:-bottom-6 sm:-mx-6 sm:p-6'
          "
        >
          <slot name="footer" />
        </footer>
      </section>
    </div>
  </Teleport>
</template>
