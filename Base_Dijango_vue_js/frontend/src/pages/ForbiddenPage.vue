<script setup lang="ts">
import AppLogo from "@/components/brand/AppLogo.vue";
import AppLink from "@/components/navigation/AppLink.vue";
</script>

<template>
  <main class="grid min-h-screen place-items-center px-4 text-center">
    <section class="max-w-md">
      <div class="mb-6 flex justify-center">
        <RouterLink to="/">
          <AppLogo variant="compact" size="md" />
        </RouterLink>
      </div>
      <p class="text-xs font-bold tracking-widest text-[var(--color-error)] uppercase">Lỗi 403</p>
      <h1
        class="mt-2 font-[var(--font-display)] text-3xl font-bold tracking-tight sm:text-4xl text-[var(--color-text)]"
      >
        Bạn không có quyền truy cập
      </h1>
      <p class="mt-3 text-sm text-[var(--color-text-muted)]">
        Tài khoản hiện tại không được cấp quyền cho khu vực này của Kim Thành Coffee.
      </p>
      <AppLink to="/" class="mt-6 inline-block" variant="button">Về trang chủ</AppLink>
    </section>
  </main>
</template>
