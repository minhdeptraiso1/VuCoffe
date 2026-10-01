<script setup lang="ts">
import RoleLayout from "./RoleLayout.vue";
</script>
<template>
  <RoleLayout
    eyebrow="Nhân viên"
    home="/employee"
    :navigation="[{ label: 'Tổng quan', to: '/employee' }]"
  >
    <slot />
  </RoleLayout>
</template>
