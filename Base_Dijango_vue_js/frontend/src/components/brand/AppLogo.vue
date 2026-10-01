<script setup lang="ts">
import { computed } from "vue";

export interface LogoProps {
  variant?: "full" | "mark" | "compact" | "pill";
  size?: "sm" | "md" | "lg" | "xl";
  showTagline?: boolean;
}

const props = withDefaults(defineProps<LogoProps>(), {
  variant: "full",
  size: "md",
  showTagline: false,
});

const sizeClasses = computed(() => {
  switch (props.size) {
    case "sm":
      return {
        icon: "w-7 h-7",
        title: "text-base tracking-wide",
        sub: "text-[0.55rem] tracking-[0.2em]",
        tagline: "text-[0.6rem]",
      };
    case "lg":
      return {
        icon: "w-12 h-12",
        title: "text-2xl tracking-wide",
        sub: "text-xs tracking-[0.25em]",
        tagline: "text-xs",
      };
    case "xl":
      return {
        icon: "w-16 h-16",
        title: "text-3xl tracking-wider",
        sub: "text-sm tracking-[0.28em]",
        tagline: "text-sm",
      };
    case "md":
    default:
      return {
        icon: "w-9 h-9",
        title: "text-lg tracking-wide",
        sub: "text-[0.65rem] tracking-[0.22em]",
        tagline: "text-[0.7rem]",
      };
  }
});
</script>

<template>
  <!-- Pill Capsule Variant (matching Caffeine reference) -->
  <div
    v-if="variant === 'pill'"
    class="inline-flex items-center gap-2 rounded-full border border-white/25 bg-white/5 px-4 py-1.5 backdrop-blur-xs transition-all hover:border-white/50 hover:bg-white/10 select-none"
    :aria-label="'Kim Thành Coffee'"
  >
    <span class="size-1.5 rounded-full bg-[var(--color-gold)] animate-pulse"></span>
    <span class="font-[var(--font-display)] text-sm font-semibold tracking-wider text-white">
      Caffeine
    </span>
    <span
      class="border-l border-white/20 pl-2 text-[0.65rem] font-medium tracking-widest text-amber-200/80 uppercase"
    >
      Kim Thành
    </span>
  </div>

  <div
    v-else
    class="inline-flex items-center gap-2.5 select-none font-sans"
    :aria-label="'Kim Thành Coffee'"
  >
    <!-- Vector Emblem Icon -->
    <div
      class="relative flex shrink-0 items-center justify-center rounded-full transition-transform duration-300 hover:scale-105"
      :class="sizeClasses.icon"
    >
      <svg
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        class="h-full w-full drop-shadow-sm"
        aria-hidden="true"
      >
        <defs>
          <!-- Gradient for outer circle seal -->
          <linearGradient id="kt-circle-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#C58940" />
            <stop offset="50%" stop-color="#8F5434" />
            <stop offset="100%" stop-color="#542E18" />
          </linearGradient>

          <!-- Gradient for inner warm badge -->
          <linearGradient id="kt-badge-grad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#FFFDF9" />
            <stop offset="100%" stop-color="#F2E6D5" />
          </linearGradient>

          <!-- Gradient for coffee cup body -->
          <linearGradient id="kt-cup-grad" x1="0%" y1="100%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#8F5434" />
            <stop offset="100%" stop-color="#4A2511" />
          </linearGradient>

          <!-- Gradient for golden steam -->
          <linearGradient id="kt-steam-grad" x1="0%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stop-color="#C58940" />
            <stop offset="100%" stop-color="#E5BA73" />
          </linearGradient>
        </defs>

        <!-- Outer Decorative Ring -->
        <circle cx="50" cy="50" r="47" stroke="url(#kt-circle-grad)" stroke-width="2.5" />
        <circle
          cx="50"
          cy="50"
          r="43"
          stroke="#D8C8B5"
          stroke-width="0.75"
          stroke-dasharray="2 2"
        />

        <!-- Inner Badge Background -->
        <circle cx="50" cy="50" r="41" fill="url(#kt-badge-grad)" />

        <!-- Coffee Cup Saucer -->
        <ellipse cx="50" cy="74" rx="26" ry="4.5" fill="#C58940" />
        <ellipse cx="50" cy="73" rx="22" ry="3" fill="#FAF5ED" />

        <!-- Coffee Cup Body -->
        <path d="M26 48 C26 67, 36 71, 50 71 C64 71, 74 67, 74 48 Z" fill="url(#kt-cup-grad)" />

        <!-- Cup Rim Highlight -->
        <ellipse cx="50" cy="48" rx="24" ry="4" fill="#3D1D0D" />
        <ellipse cx="50" cy="48" rx="21" ry="2.8" fill="#60341E" />
        <!-- Golden Crema in Cup -->
        <ellipse cx="50" cy="48" rx="18" ry="2" fill="#D4A373" />

        <!-- Coffee Cup Handle -->
        <path
          d="M72 51 C79 51, 84 55, 84 61 C84 66, 78 68, 70 67"
          stroke="#7A4222"
          stroke-width="3.5"
          stroke-linecap="round"
          fill="none"
        />

        <!-- Stylized Coffee Bean on Cup Center -->
        <g transform="translate(50, 60)">
          <!-- Bean left lobe -->
          <path
            d="M -1 -6 C -6 -6, -8 -1, -8 2 C -8 5, -5 8, -1 8 C -2 3, -2 -2, -1 -6 Z"
            fill="#E5BA73"
          />
          <!-- Bean right lobe -->
          <path d="M 1 -6 C 6 -6, 8 -1, 8 2 C 8 5, 5 8, 1 8 C 2 3, 2 -2, 1 -6 Z" fill="#E5BA73" />
          <!-- S-curve center line of coffee bean -->
          <path
            d="M -0.5 -5 C 2 -2, -2 2, 0.5 7"
            stroke="#542E18"
            stroke-width="1.2"
            stroke-linecap="round"
            fill="none"
          />
        </g>

        <!-- Aromatic Steam Swirls with Golden Glow -->
        <!-- Center main steam plume (sprouting like young coffee leaf) -->
        <path
          d="M50 43 C47 36, 54 31, 50 22 C48 18, 45 16, 47 13"
          stroke="url(#kt-steam-grad)"
          stroke-width="2.6"
          stroke-linecap="round"
          fill="none"
        />
        <!-- Left gentle steam swirl -->
        <path
          d="M42 41 C37 35, 41 29, 39 23 C38 20, 36 19, 37 16"
          stroke="url(#kt-steam-grad)"
          stroke-width="1.8"
          stroke-linecap="round"
          opacity="0.85"
          fill="none"
        />
        <!-- Right delicate steam swirl -->
        <path
          d="M58 41 C63 35, 60 28, 62 23"
          stroke="url(#kt-steam-grad)"
          stroke-width="1.8"
          stroke-linecap="round"
          opacity="0.85"
          fill="none"
        />

        <!-- Little Aroma Star / Sparkle at top -->
        <circle cx="50" cy="11" r="1.5" fill="#C58940" />
      </svg>
    </div>

    <!-- Brand Typography -->
    <div v-if="variant !== 'mark'" class="flex flex-col justify-center leading-none">
      <div v-if="variant === 'compact'" class="flex items-baseline gap-1.5">
        <span
          class="font-[var(--font-display)] font-bold text-[var(--color-primary)]"
          :class="sizeClasses.title"
        >
          Kim Thành
        </span>
        <span class="font-semibold text-[var(--color-accent)] uppercase" :class="sizeClasses.sub">
          Coffee
        </span>
      </div>

      <template v-else>
        <span
          class="font-[var(--font-display)] font-bold text-[var(--color-primary)] tracking-wide"
          :class="sizeClasses.title"
        >
          KIM THÀNH
        </span>
        <div class="flex items-center gap-1 mt-0.5">
          <span class="h-[1px] w-2 bg-[var(--color-accent)] opacity-60"></span>
          <span class="font-bold text-[var(--color-accent)] uppercase" :class="sizeClasses.sub">
            COFFEE
          </span>
          <span class="h-[1px] w-2 bg-[var(--color-accent)] opacity-60"></span>
        </div>
        <p
          v-if="showTagline"
          class="mt-1 text-[var(--color-text-muted)] font-normal italic"
          :class="sizeClasses.tagline"
        >
          Rang mộc · Đậm vị truyền thống
        </p>
      </template>
    </div>
  </div>
</template>
