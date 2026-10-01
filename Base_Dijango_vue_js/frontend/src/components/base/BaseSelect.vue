<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, ref } from "vue";
import { Check, ChevronDown } from "lucide-vue-next";

defineOptions({ inheritAttrs: false });
export interface SelectOption {
  label: string;
  value: string;
  disabled?: boolean;
}
interface Props {
  modelValue: string;
  id: string;
  name: string;
  options: SelectOption[];
  placeholder?: string;
  disabled?: boolean;
  required?: boolean;
  invalid?: boolean;
}
const props = withDefaults(defineProps<Props>(), {
  placeholder: "Chọn một giá trị",
  disabled: false,
  required: false,
  invalid: false,
});
const emit = defineEmits<{ "update:modelValue": [value: string]; blur: [event: FocusEvent] }>();
const open = ref(false);
const activeIndex = ref(0);
const root = ref<HTMLElement | null>(null);
const listbox = ref<HTMLElement | null>(null);
const selected = computed(() => props.options.find((item) => item.value === props.modelValue));

function close() {
  open.value = false;
}
function toggle() {
  if (props.disabled) return;
  open.value = !open.value;
  activeIndex.value = Math.max(
    0,
    props.options.findIndex((item) => item.value === props.modelValue),
  );
  if (open.value) void nextTick(() => listbox.value?.focus());
}
function choose(index: number) {
  const option = props.options[index];
  if (!option || option.disabled) return;
  emit("update:modelValue", option.value);
  close();
  root.value?.querySelector<HTMLButtonElement>("button")?.focus();
}
function move(delta: number) {
  let next = activeIndex.value;
  do next = (next + delta + props.options.length) % props.options.length;
  while (props.options[next]?.disabled && next !== activeIndex.value);
  activeIndex.value = next;
}
function onKeydown(event: KeyboardEvent) {
  if (["ArrowDown", "ArrowUp", "Home", "End", "Enter", " ", "Escape"].includes(event.key))
    event.preventDefault();
  if (event.key === "Escape") {
    close();
    return;
  }
  if (!open.value) {
    toggle();
    return;
  }
  if (event.key === "ArrowDown") move(1);
  if (event.key === "ArrowUp") move(-1);
  if (event.key === "Home") activeIndex.value = 0;
  if (event.key === "End") activeIndex.value = props.options.length - 1;
  if (event.key === "Enter" || event.key === " ") choose(activeIndex.value);
}
function outside(event: MouseEvent) {
  if (!root.value?.contains(event.target as Node)) close();
}
globalThis.document.addEventListener("mousedown", outside);
onBeforeUnmount(() => {
  globalThis.document.removeEventListener("mousedown", outside);
});
</script>

<template>
  <div ref="root" class="relative w-full" v-bind="$attrs">
    <input type="hidden" :name="name" :value="modelValue" />
    <button
      :id="id"
      type="button"
      role="combobox"
      :aria-expanded="open"
      :aria-controls="`${id}-options`"
      :aria-invalid="invalid || undefined"
      :disabled="disabled"
      class="flex min-h-11 w-full items-center justify-between gap-3 rounded-[var(--radius-sm)] border bg-[var(--color-surface)] px-3 text-left text-sm shadow-sm transition disabled:cursor-not-allowed disabled:opacity-55"
      :class="
        invalid
          ? 'border-[var(--color-error)]'
          : 'border-[var(--color-border)] hover:border-[var(--color-primary)]'
      "
      @click="toggle"
      @keydown="onKeydown"
      @blur="emit('blur', $event)"
    >
      <span :class="!selected && 'text-[var(--color-text-muted)]'">{{
        selected?.label || placeholder
      }}</span>
      <ChevronDown
        class="size-4 shrink-0 transition-transform"
        :class="open && 'rotate-180'"
        aria-hidden="true"
      />
    </button>
    <div
      v-if="open"
      :id="`${id}-options`"
      ref="listbox"
      role="listbox"
      tabindex="-1"
      :aria-activedescendant="`${id}-option-${activeIndex}`"
      class="absolute z-50 mt-1 max-h-64 w-full overflow-auto rounded-[var(--radius-sm)] border border-[var(--color-border)] bg-[var(--color-surface)] p-1 shadow-[var(--shadow-overlay)]"
      @keydown="onKeydown"
    >
      <button
        v-for="(option, index) in options"
        :id="`${id}-option-${index}`"
        :key="option.value"
        type="button"
        role="option"
        :aria-selected="modelValue === option.value"
        :disabled="option.disabled"
        class="flex min-h-10 w-full items-center justify-between rounded px-3 text-left text-sm hover:bg-[var(--color-primary-soft)] disabled:opacity-40"
        :class="activeIndex === index && 'bg-[var(--color-primary-soft)]'"
        @mouseenter="activeIndex = index"
        @click="choose(index)"
      >
        {{ option.label
        }}<Check v-if="modelValue === option.value" class="size-4 text-[var(--color-primary)]" />
      </button>
    </div>
  </div>
</template>
