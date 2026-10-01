<script setup lang="ts">
import {
  ArrowRight,
  Database,
  FileSpreadsheet,
  PackageOpen,
  ShieldCheck,
  UsersRound,
} from "lucide-vue-next";
import AppBadge from "@/components/data/AppBadge.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";
</script>

<template>
  <AdminLayout>
    <section
      class="rounded-[var(--radius-lg)] bg-[var(--color-espresso-dark)] p-6 text-white sm:p-8"
    >
      <AppBadge variant="warning">Trung tâm điều hành</AppBadge>
      <h1 class="mt-4 max-w-2xl font-[var(--font-display)] text-3xl font-bold sm:text-4xl">
        Quản lý Kim Thành Coffee
      </h1>
      <p class="mt-3 max-w-2xl text-sm leading-relaxed text-stone-300 sm:text-base">
        Theo dõi tài khoản nội bộ, phân quyền nhân viên và quản lý thông tin quản trị tại một nơi
        thống nhất.
      </p>
    </section>

    <section class="mt-8" aria-labelledby="admin-actions-title">
      <div class="flex items-end justify-between gap-4">
        <div>
          <p class="text-xs font-bold uppercase tracking-[0.16em] text-[var(--color-primary)]">
            Công cụ quản trị
          </p>
          <h2 id="admin-actions-title" class="mt-1 font-[var(--font-display)] text-2xl font-bold">
            Tác vụ thường dùng
          </h2>
        </div>
        <p class="hidden text-sm text-[var(--color-text-muted)] sm:block">
          Chọn một khu vực để bắt đầu
        </p>
      </div>
      <div class="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <RouterLink
          to="/admin/employees"
          class="group rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 shadow-sm transition hover:border-[var(--color-primary)] hover:shadow-[var(--shadow-surface)]"
          ><div
            class="flex size-10 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-primary-soft)] text-[var(--color-primary)]"
          >
            <UsersRound class="size-5" aria-hidden="true" />
          </div>
          <h3 class="mt-5 text-lg font-bold">Nhân viên và phân quyền</h3>
          <p class="mt-2 text-sm leading-relaxed text-[var(--color-text-muted)]">
            Tạo tài khoản nhân viên, xem trạng thái và kiểm soát quyền nghiệp vụ.
          </p>
          <span
            class="mt-5 inline-flex items-center gap-2 text-sm font-bold text-[var(--color-primary)]"
            >Mở quản lý
            <ArrowRight class="size-4 transition-transform group-hover:translate-x-1" /></span
        ></RouterLink>
        <RouterLink
          to="/admin/catalog"
          class="group rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 shadow-sm transition hover:border-[var(--color-primary)] hover:shadow-[var(--shadow-surface)]"
          ><div
            class="flex size-10 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-primary-soft)] text-[var(--color-primary)]"
          >
            <PackageOpen class="size-5" aria-hidden="true" />
          </div>
          <h3 class="mt-5 text-lg font-bold">Thực đơn và giá bán</h3>
          <p class="mt-2 text-sm leading-relaxed text-[var(--color-text-muted)]">
            Quản lý danh mục, món, kích cỡ, giá bán và các món thêm hợp lệ.
          </p>
          <span
            class="mt-5 inline-flex items-center gap-2 text-sm font-bold text-[var(--color-primary)]"
            >Mở quản lý
            <ArrowRight class="size-4 transition-transform group-hover:translate-x-1" /></span
        ></RouterLink>
        <RouterLink
          to="/admin/inventory"
          class="group rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 shadow-sm transition hover:border-[var(--color-primary)]"
          ><div
            class="flex size-10 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-primary-soft)] text-[var(--color-primary)]"
          >
            <Database class="size-5" />
          </div>
          <h3 class="mt-5 text-lg font-bold">Nguyên liệu và công thức</h3>
          <p class="mt-2 text-sm leading-relaxed text-[var(--color-text-muted)]">
            Chuẩn hóa đơn vị, nhà cung cấp và định lượng cho từng món.
          </p>
          <span
            class="mt-5 inline-flex items-center gap-2 text-sm font-bold text-[var(--color-primary)]"
            >Mở quản lý<ArrowRight class="size-4" /></span
        ></RouterLink>
        <RouterLink
          to="/admin/imports"
          class="group rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 shadow-sm transition hover:border-[var(--color-primary)]"
          ><div
            class="flex size-10 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-primary-soft)] text-[var(--color-primary)]"
          >
            <FileSpreadsheet class="size-5" />
          </div>
          <h3 class="mt-5 text-lg font-bold">Nhập và xuất Excel</h3>
          <p class="mt-2 text-sm leading-relaxed text-[var(--color-text-muted)]">
            Xem trước, kiểm tra lỗi rồi mới xác nhận dữ liệu hàng loạt.
          </p>
          <span
            class="mt-5 inline-flex items-center gap-2 text-sm font-bold text-[var(--color-primary)]"
            >Mở công cụ<ArrowRight class="size-4" /></span
        ></RouterLink>
        <div
          class="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5 shadow-sm"
        >
          <div
            class="flex size-10 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-success-soft)] text-[var(--color-success)]"
          >
            <ShieldCheck class="size-5" aria-hidden="true" />
          </div>
          <h3 class="mt-5 text-lg font-bold">Bảo vệ truy cập</h3>
          <p class="mt-2 text-sm leading-relaxed text-[var(--color-text-muted)]">
            Mọi trang quản trị đều kiểm tra vai trò; backend tiếp tục xác thực quyền cho từng yêu
            cầu.
          </p>
          <AppBadge class="mt-5" variant="success">Đang hoạt động</AppBadge>
        </div>
      </div>
    </section>
  </AdminLayout>
</template>
