<script setup lang="ts">
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { ArrowRight, ShieldCheck, UserRound } from "lucide-vue-next";
import AppBadge from "@/components/data/AppBadge.vue";
import AppEmptyState from "@/components/feedback/AppEmptyState.vue";
import EmployeeLayout from "@/layouts/EmployeeLayout.vue";
import { useAuthStore } from "@/modules/auth/stores/auth";
import { permissionLabel } from "@/modules/employees/utils/permissionLabels";

const auth = useAuthStore();
const { user } = storeToRefs(auth);
const permissionCount = computed(() => user.value?.permissions.length ?? 0);
</script>

<template>
  <EmployeeLayout>
    <section
      class="rounded-[var(--radius-lg)] bg-[var(--color-espresso-dark)] p-6 text-white sm:p-8"
    >
      <AppBadge variant="warning">Khu vực nhân viên</AppBadge>
      <h1 class="mt-4 font-[var(--font-display)] text-3xl font-bold sm:text-4xl">
        Xin chào, {{ user?.full_name || "nhân viên" }}
      </h1>
      <p class="mt-3 max-w-2xl text-sm leading-relaxed text-stone-300 sm:text-base">
        Đây là không gian làm việc nội bộ. Các công cụ được hiển thị theo đúng quyền quản trị viên
        đã cấp cho tài khoản của bạn.
      </p>
    </section>

    <div class="mt-8 grid gap-4 lg:grid-cols-[1.35fr_0.65fr]">
      <section
        class="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 sm:p-6"
        aria-labelledby="employee-permissions-title"
      >
        <div class="flex items-center justify-between gap-4">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.16em] text-[var(--color-primary)]">
              Phạm vi truy cập
            </p>
            <h2 id="employee-permissions-title" class="mt-1 text-xl font-bold">
              Quyền đang được cấp
            </h2>
          </div>
          <AppBadge :variant="permissionCount ? 'success' : 'warning'"
            >{{ permissionCount }} quyền</AppBadge
          >
        </div>
        <ul v-if="user?.permissions.length" class="mt-5 grid gap-2 sm:grid-cols-2">
          <li
            v-for="permission in user.permissions"
            :key="permission"
            class="rounded-[var(--radius-sm)] bg-[var(--color-surface-subtle)] px-3 py-2 text-sm font-medium"
          >
            {{ permissionLabel(permission) }}
          </li>
        </ul>
        <AppEmptyState
          v-else
          class="mt-5"
          title="Chưa có quyền nghiệp vụ"
          description="Liên hệ quản trị viên nếu bạn cần thêm quyền để thực hiện công việc."
        />
      </section>
      <section class="space-y-4">
        <RouterLink
          to="/profile"
          class="group block rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 hover:border-[var(--color-primary)]"
          ><UserRound class="size-5 text-[var(--color-primary)]" />
          <h2 class="mt-4 font-bold">Hồ sơ cá nhân</h2>
          <p class="mt-1 text-sm text-[var(--color-text-muted)]">
            Kiểm tra email và cập nhật tên hiển thị.
          </p>
          <span
            class="mt-4 inline-flex items-center gap-2 text-sm font-bold text-[var(--color-primary)]"
            >Mở hồ sơ <ArrowRight class="size-4" /></span
        ></RouterLink>
        <div
          class="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
        >
          <ShieldCheck class="size-5 text-[var(--color-success)]" />
          <h2 class="mt-4 font-bold">Phiên làm việc an toàn</h2>
          <p class="mt-1 text-sm text-[var(--color-text-muted)]">
            Quyền bị thu hồi sẽ được cập nhật từ lần kiểm tra phiên tiếp theo.
          </p>
        </div>
      </section>
    </div>
  </EmployeeLayout>
</template>
