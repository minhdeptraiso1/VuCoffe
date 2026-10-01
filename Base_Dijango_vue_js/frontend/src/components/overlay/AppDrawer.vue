<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref, watch } from "vue";

interface Props {
  open: boolean;
  title: string;
  description?: string;
  closeLabel?: string;
}

const props = withDefaults(defineProps<Props>(), {
  description: "",
  closeLabel: "Đóng ngăn kéo",
});
const emit = defineEmits<{ close: [] }>();
const drawer = ref<HTMLElement | null>(null);
let previousFocus: HTMLElement | null = null;

function focusableElements() {
  return Array.from(
    drawer.value?.querySelectorAll<HTMLElement>(
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
    <Transition name="drawer">
      <div
        v-if="props.open"
        class="fixed inset-0 z-[var(--z-overlay)] flex justify-end bg-[var(--color-overlay)]"
        @mousedown.self="emit('close')"
      >
        <aside
          ref="drawer"
          role="dialog"
          aria-modal="true"
          :aria-labelledby="`${$attrs.id ?? 'app-drawer'}-title`"
          :aria-describedby="
            props.description ? `${$attrs.id ?? 'app-drawer'}-description` : undefined
          "
          class="flex h-full w-full max-w-md flex-col bg-[var(--color-surface)] shadow-[var(--shadow-overlay)]"
          @keydown="onKeydown"
        >
          <header
            class="flex items-start justify-between gap-4 border-b border-[var(--color-border)] p-5"
          >
            <div>
              <h2
                :id="`${$attrs.id ?? 'app-drawer'}-title`"
                class="font-[var(--font-display)] text-2xl font-bold"
              >
                {{ props.title }}
              </h2>
              <p
                v-if="props.description"
                :id="`${$attrs.id ?? 'app-drawer'}-description`"
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
          <div class="min-h-0 flex-1 overflow-y-auto p-5"><slot /></div>
          <footer
            v-if="$slots.footer"
            class="border-t border-[var(--color-border)] bg-[var(--color-surface)] p-5"
          >
            <slot name="footer" />
          </footer>
        </aside>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity var(--transition-base);
}
.drawer-enter-active aside,
.drawer-leave-active aside {
  transition: transform var(--transition-base);
}
.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}
.drawer-enter-from aside,
.drawer-leave-to aside {
  transform: translateX(100%);
}
</style>
