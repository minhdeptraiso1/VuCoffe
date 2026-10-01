<script setup lang="ts">
import AppLogo from "@/components/brand/AppLogo.vue";
</script>

<template>
  <main class="relative grid min-h-screen place-items-center px-4 py-10 sm:px-6 overflow-hidden">
    <!-- Ambient Coffee Aroma Lighting -->
    <div
      class="pointer-events-none absolute -top-24 -left-24 size-80 rounded-full bg-[var(--color-primary-soft)] opacity-50 blur-3xl"
    ></div>
    <div
      class="pointer-events-none absolute -bottom-24 -right-24 size-80 rounded-full bg-[var(--color-gold-soft,#fbf3e6)] opacity-60 blur-3xl"
    ></div>

    <section
      class="relative w-full max-w-md rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-6 shadow-[var(--shadow-surface)] sm:p-8 backdrop-blur-sm"
    >
      <header class="mb-8 text-center sm:text-left">
        <!-- Logo Header -->
        <div class="mb-5 flex justify-center sm:justify-start">
          <RouterLink to="/" class="no-underline">
            <AppLogo variant="compact" size="md" />
          </RouterLink>
        </div>

        <h1
          class="font-[var(--font-display)] text-2xl font-bold tracking-tight text-[var(--color-text)] sm:text-3xl"
        >
          <slot name="title" />
        </h1>
        <p class="mt-2 text-sm text-[var(--color-text-muted)] leading-relaxed">
          <slot name="subtitle" />
        </p>
      </header>

      <slot />

      <!-- Back to home link -->
      <footer class="mt-6 pt-5 border-t border-[var(--color-border)]/60 text-center">
        <RouterLink
          to="/"
          class="text-xs text-[var(--color-text-muted)] hover:text-[var(--color-primary)] transition-colors inline-flex items-center gap-1"
        >
          ← Quay lại trang chủ Kim Thành Coffee
        </RouterLink>
      </footer>
    </section>
  </main>
</template>
