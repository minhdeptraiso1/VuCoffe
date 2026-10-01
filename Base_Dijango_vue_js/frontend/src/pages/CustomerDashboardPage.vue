<script setup lang="ts">
import AppBadge from "@/components/data/AppBadge.vue";
import AppCard from "@/components/surface/AppCard.vue";
import CustomerLayout from "@/layouts/CustomerLayout.vue";
</script>

<template>
  <CustomerLayout>
    <div class="space-y-6">
      <header class="border-b border-[var(--color-border)] pb-6">
        <div class="flex items-center justify-between">
          <AppBadge variant="warning">Thành viên Kim Thành Club</AppBadge>
          <div class="flex flex-wrap justify-end gap-2">
            <RouterLink
              to="/profile"
              class="inline-flex min-h-10 items-center rounded-full border border-[var(--color-border)] bg-white px-4 text-xs font-semibold text-[var(--color-text)] transition-all hover:border-[var(--color-primary)] hover:bg-stone-50"
            >
              Hồ sơ cá nhân
            </RouterLink>
            <RouterLink
              to="/"
              class="inline-flex min-h-10 items-center rounded-full border border-[var(--color-border)] bg-white px-4 text-xs font-semibold text-[var(--color-text)] transition-all hover:border-[var(--color-primary)] hover:bg-stone-50"
            >
              ← Về trang chủ
            </RouterLink>
          </div>
        </div>
        <h1
          class="mt-3 font-[var(--font-display)] text-3xl font-bold sm:text-4xl text-[var(--color-text)]"
        >
          Chào mừng bạn đến với Kim Thành Coffee
        </h1>
        <p class="mt-2 text-[var(--color-text-muted)] text-base">
          Theo dõi lịch sử gọi món, tích điểm thưởng và tận hưởng những đặc quyền ưu đãi dành riêng
          cho bạn.
        </p>
      </header>

      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <AppCard title="Hạng thành viên" description="Tích lũy từ các đơn hàng">
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-2xl font-bold text-[var(--color-primary)] font-[var(--font-display)]">
              Thành Viên Mới
            </span>
            <AppBadge variant="success">Hoạt động</AppBadge>
          </div>
          <p class="mt-3 text-xs text-[var(--color-text-muted)]">
            Tặng ngay voucher giảm 15% cho đơn hàng đầu tiên tại quầy hoặc đặt trước.
          </p>
        </AppCard>

        <AppCard title="Điểm hạt cà phê" description="Quy đổi đồ uống miễn phí">
          <div class="mt-2 flex items-baseline gap-2">
            <span class="text-3xl font-bold text-[var(--color-accent)] font-[var(--font-display)]">
              50
            </span>
            <span class="text-xs text-[var(--color-text-muted)]">điểm</span>
          </div>
          <p class="mt-3 text-xs text-[var(--color-text-muted)]">
            Đạt 100 điểm để đổi 1 ly Cà phê Muối Kim Thành bất kỳ.
          </p>
        </AppCard>

        <AppCard title="Đặt món nhanh" description="Thực đơn trực tuyến">
          <RouterLink
            to="/menu"
            class="mt-2 inline-flex items-center gap-1 font-semibold text-[var(--color-primary)] hover:text-[var(--color-accent)] transition-colors"
          >
            Xem thực đơn hôm nay →
          </RouterLink>
          <p class="mt-3 text-xs text-[var(--color-text-muted)]">
            Quầy mở cửa phục vụ từ 07:00 đến 22:30 hàng ngày.
          </p>
        </AppCard>
      </div>

      <AppCard title="Trạng thái tài khoản" class="mt-6">
        <div class="flex items-center justify-between">
          <div class="space-y-1">
            <p class="text-sm font-medium text-[var(--color-text)]">Tài khoản xác thực an toàn</p>
            <p class="text-xs text-[var(--color-text-muted)]">
              Phiên đăng nhập được bảo vệ bởi HttpOnly cookie và CSRF token.
            </p>
          </div>
          <AppBadge variant="success">Đã kích hoạt</AppBadge>
        </div>
      </AppCard>
    </div>
  </CustomerLayout>
</template>
