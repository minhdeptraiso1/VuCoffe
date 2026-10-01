<script setup lang="ts">
import { ref } from "vue";
import { useCoffeeScene } from "../composables/useCoffeeScene";

const canvas = ref<HTMLCanvasElement | null>(null);
const { status } = useCoffeeScene(canvas);
</script>

<template>
  <div
    class="relative min-h-[22rem] sm:min-h-[28rem] overflow-hidden rounded-[2rem] bg-gradient-to-b from-[#FAF4EB] via-[#F4E9DB] to-[#E9D8C3] shadow-inner select-none"
    aria-label="Minh họa mô hình 3D tách cà phê Kim Thành"
  >
    <!-- Warm Ambient Spotlight Behind the Cup -->
    <div
      class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_45%,rgba(255,255,255,0.85)_0%,rgba(240,225,206,0.5)_50%,transparent_75%)]"
    ></div>

    <!-- Fallback Illustration while loading or on error -->
    <div
      aria-hidden="true"
      class="absolute inset-0 grid place-items-center transition-opacity pointer-events-none"
      :class="status === 'ready' ? 'opacity-0' : 'opacity-100'"
    >
      <div
        class="relative h-40 w-48 rounded-b-[4rem] rounded-t-[1.5rem] bg-[#efd4b5] shadow-[0_24px_40px_rgb(87_48_29_/_0.2)]"
      >
        <span
          class="absolute -right-12 top-8 h-20 w-20 rounded-full border-[1.1rem] border-[#efd4b5]"
        ></span>
        <span class="absolute inset-x-3 top-2 h-5 rounded-full bg-[#3b2015]"></span>
      </div>
    </div>

    <!-- WebGL Canvas with Grab Cursor -->
    <canvas
      ref="canvas"
      class="absolute inset-0 size-full cursor-grab active:cursor-grabbing touch-none"
      :class="status === 'ready' ? 'opacity-100' : 'opacity-0'"
      aria-label="Mô hình 3D tương tác tách cà phê"
    ></canvas>

    <!-- Floating Interactive Hint Badge -->
    <div class="pointer-events-none absolute bottom-3.5 inset-x-0 flex justify-center px-4">
      <span
        class="inline-flex items-center gap-1.5 rounded-full bg-white/80 px-3 py-1 text-[0.7rem] font-semibold text-[var(--color-primary)] shadow-sm backdrop-blur-sm border border-[var(--color-border)]/50"
      >
        <span>🔄</span> Kéo để xoay 360°
      </span>
    </div>

    <p v-if="status === 'error'" class="sr-only">
      Thiết bị không hỗ trợ WebGL; đang dùng minh họa tĩnh.
    </p>
  </div>
</template>
