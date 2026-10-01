<script setup lang="ts">
import RoleLayout from "./RoleLayout.vue";
</script>
<template>
  <RoleLayout
    eyebrow="Quản trị"
    home="/admin"
    :navigation="[
      { label: 'Tổng quan', to: '/admin' },
      { label: 'Nhân viên', to: '/admin/employees' },
      { label: 'Thực đơn', to: '/admin/catalog' },
      { label: 'Nguyên liệu & công thức', to: '/admin/inventory' },
      { label: 'Nhập & xuất Excel', to: '/admin/imports' },
    ]"
  >
    <slot />
  </RoleLayout>
</template>
