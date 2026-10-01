<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { KeyRound, Plus } from "lucide-vue-next";

import { useToastStore } from "@/app/stores/toast";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseCheckbox from "@/components/base/BaseCheckbox.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import AppBadge from "@/components/data/AppBadge.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import AppEmptyState from "@/components/feedback/AppEmptyState.vue";
import FormField from "@/components/form/FormField.vue";
import AppModal from "@/components/overlay/AppModal.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";
import { toAppError } from "@/lib/http/errors";
import type { User } from "@/modules/auth/types";
import {
  createEmployeeRequest,
  employeesRequest,
  permissionCatalogRequest,
  updateEmployeePermissionsRequest,
} from "../api/employee.api";
import type { PermissionOption } from "../types/employee.types";
import { permissionDescription, permissionLabel } from "../utils/permissionLabels";

const toast = useToastStore();
const employees = ref<User[]>([]);
const permissions = ref<PermissionOption[]>([]);
const count = ref(0);
const page = ref(1);
const hasNext = ref(false);
const hasPrevious = ref(false);
const loading = ref(true);
const loadError = ref("");
const createOpen = ref(false);
const createLoading = ref(false);
const createError = ref("");
const createFields = ref<Record<string, string>>({});
const createForm = reactive({ email: "", full_name: "", password: "" });
const permissionsOpen = ref(false);
const permissionLoading = ref(false);
const permissionError = ref("");
const activeEmployee = ref<User | null>(null);
const selectedPermissions = ref<string[]>([]);
const pageSummary = computed(
  () => `Trang ${String(page.value)} · ${String(count.value)} nhân viên`,
);

async function loadData(targetPage = page.value) {
  loading.value = true;
  loadError.value = "";
  try {
    const [employeePage, permissionOptions] = await Promise.all([
      employeesRequest(targetPage),
      permissions.value.length ? Promise.resolve(permissions.value) : permissionCatalogRequest(),
    ]);
    employees.value = employeePage.results;
    permissions.value = permissionOptions;
    count.value = employeePage.count;
    page.value = targetPage;
    hasNext.value = Boolean(employeePage.next);
    hasPrevious.value = Boolean(employeePage.previous);
  } catch (error) {
    loadError.value = toAppError(error).message;
    toast.show(loadError.value, "error");
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  createError.value = "";
  createFields.value = {};
  createOpen.value = true;
}

async function createEmployee() {
  createLoading.value = true;
  createError.value = "";
  createFields.value = {};
  try {
    await createEmployeeRequest({ ...createForm });
    createOpen.value = false;
    Object.assign(createForm, { email: "", full_name: "", password: "" });
    toast.show("Đã tạo tài khoản nhân viên.", "success");
    await loadData(1);
  } catch (error) {
    const appError = toAppError(error);
    createError.value = appError.message;
    createFields.value = appError.fields;
    toast.show(appError.message, "error");
  } finally {
    createLoading.value = false;
  }
}

function openPermissions(employee: User) {
  activeEmployee.value = employee;
  selectedPermissions.value = [...employee.permissions];
  permissionError.value = "";
  permissionsOpen.value = true;
}

function updateSelectedPermission(code: string, selected: boolean) {
  selectedPermissions.value = selected
    ? [...selectedPermissions.value, code]
    : selectedPermissions.value.filter((value) => value !== code);
}

async function savePermissions() {
  if (!activeEmployee.value) return;
  permissionLoading.value = true;
  permissionError.value = "";
  try {
    const updated = await updateEmployeePermissionsRequest(
      activeEmployee.value.id,
      selectedPermissions.value,
    );
    employees.value = employees.value.map((employee) =>
      employee.id === updated.id ? updated : employee,
    );
    permissionsOpen.value = false;
    toast.show(`Đã cập nhật quyền cho ${updated.full_name || updated.email}.`, "success");
  } catch (error) {
    permissionError.value = toAppError(error).message;
    toast.show(permissionError.value, "error");
  } finally {
    permissionLoading.value = false;
  }
}

onMounted(() => {
  void loadData();
});
</script>

<template>
  <AdminLayout>
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="text-xs font-bold uppercase tracking-[0.18em] text-[var(--color-primary)]">
          Tài khoản nội bộ
        </p>
        <h1 class="mt-1 font-[var(--font-display)] text-4xl font-bold">Quản lý nhân viên</h1>
        <p class="mt-2 text-[var(--color-text-muted)]">
          Tạo tài khoản và chỉ cấp các quyền nghiệp vụ nằm trong danh mục an toàn.
        </p>
      </div>
      <BaseButton @click="openCreate"
        ><Plus class="size-4" aria-hidden="true" />Thêm nhân viên</BaseButton
      >
    </div>

    <AppAlert v-if="loadError" class="mt-6" variant="error" title="Chưa tải được dữ liệu"
      >{{ loadError }}
      <div class="mt-3">
        <BaseButton size="sm" variant="secondary" @click="loadData()">Thử lại</BaseButton>
      </div></AppAlert
    >
    <div
      v-else-if="loading"
      class="mt-6 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-8 text-center text-sm text-[var(--color-text-muted)]"
      role="status"
    >
      Đang tải danh sách nhân viên…
    </div>
    <AppEmptyState
      v-else-if="employees.length === 0"
      class="mt-6 bg-[var(--color-surface)]"
      title="Chưa có nhân viên"
      description="Tạo tài khoản nhân viên đầu tiên để bắt đầu phân quyền."
      ><template #action
        ><BaseButton @click="openCreate">Thêm nhân viên</BaseButton></template
      ></AppEmptyState
    >
    <section
      v-else
      class="mt-6 overflow-hidden rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)]"
      aria-label="Danh sách nhân viên"
    >
      <div
        class="hidden grid-cols-[1.4fr_1.5fr_0.7fr_auto] gap-4 border-b border-[var(--color-border)] bg-[var(--color-surface-subtle)] px-5 py-3 text-xs font-bold uppercase tracking-wider text-[var(--color-text-muted)] md:grid"
      >
        <span>Nhân viên</span><span>Email</span><span>Quyền</span><span>Thao tác</span>
      </div>
      <article
        v-for="employee in employees"
        :key="employee.id"
        class="grid gap-3 border-b border-[var(--color-border)] p-5 last:border-b-0 md:grid-cols-[1.4fr_1.5fr_0.7fr_auto] md:items-center"
      >
        <div>
          <h2 class="font-semibold">{{ employee.full_name || "Chưa cập nhật tên" }}</h2>
          <AppBadge class="mt-1" :variant="employee.is_active ? 'success' : 'error'">{{
            employee.is_active ? "Đang hoạt động" : "Đã khóa"
          }}</AppBadge>
        </div>
        <p class="break-all text-sm text-[var(--color-text-muted)]">{{ employee.email }}</p>
        <p class="text-sm">
          <strong>{{ employee.permissions.length }}</strong> quyền
        </p>
        <BaseButton size="sm" variant="secondary" @click="openPermissions(employee)"
          ><KeyRound class="size-4" aria-hidden="true" />Phân quyền</BaseButton
        >
      </article>
      <footer
        class="flex items-center justify-between gap-3 border-t border-[var(--color-border)] px-5 py-4"
      >
        <span class="text-sm text-[var(--color-text-muted)]">{{ pageSummary }}</span>
        <div class="flex gap-2">
          <BaseButton
            size="sm"
            variant="secondary"
            :disabled="!hasPrevious"
            @click="loadData(page - 1)"
            >Trang trước</BaseButton
          ><BaseButton
            size="sm"
            variant="secondary"
            :disabled="!hasNext"
            @click="loadData(page + 1)"
            >Trang sau</BaseButton
          >
        </div>
      </footer>
    </section>

    <AppModal
      id="create-employee"
      :open="createOpen"
      title="Thêm nhân viên"
      description="Tài khoản mới được gán vai trò nhân viên và chưa có quyền nghiệp vụ."
      @close="createOpen = false"
    >
      <form class="space-y-4" @submit.prevent="createEmployee">
        <AppAlert v-if="createError" variant="error">{{ createError }}</AppAlert>
        <FormField
          v-slot="field"
          label="Họ và tên"
          name="employee-full-name"
          :error="createFields.full_name"
          required
          ><BaseInput
            :id="field.id"
            v-model="createForm.full_name"
            name="full_name"
            autocomplete="name"
            :invalid="field.invalid"
            :aria-describedby="field.describedBy"
            required
        /></FormField>
        <FormField
          v-slot="field"
          label="Email"
          name="employee-email"
          :error="createFields.email"
          required
          ><BaseInput
            :id="field.id"
            v-model="createForm.email"
            name="email"
            type="email"
            autocomplete="email"
            :invalid="field.invalid"
            :aria-describedby="field.describedBy"
            required
        /></FormField>
        <FormField
          v-slot="field"
          label="Mật khẩu ban đầu"
          name="employee-password"
          help="Dùng mật khẩu đủ mạnh theo chính sách của máy chủ."
          :error="createFields.password"
          required
          ><BaseInput
            :id="field.id"
            v-model="createForm.password"
            name="password"
            type="password"
            autocomplete="new-password"
            :invalid="field.invalid"
            :aria-describedby="field.describedBy"
            required
        /></FormField>
        <div class="flex justify-end gap-3 pt-2">
          <BaseButton variant="secondary" @click="createOpen = false">Hủy</BaseButton
          ><BaseButton type="submit" :loading="createLoading">Tạo nhân viên</BaseButton>
        </div>
      </form>
    </AppModal>

    <AppModal
      id="employee-permissions"
      :open="permissionsOpen"
      title="Phân quyền nhân viên"
      :description="
        activeEmployee
          ? `${activeEmployee.full_name || activeEmployee.email} · quyền có hiệu lực từ lần kiểm tra phiên tiếp theo`
          : ''
      "
      @close="permissionsOpen = false"
    >
      <AppAlert v-if="permissionError" class="mb-4" variant="error">{{ permissionError }}</AppAlert>
      <AppEmptyState
        v-if="permissions.length === 0"
        title="Không có quyền có thể cấp"
        description="Máy chủ chưa trả về quyền nghiệp vụ an toàn."
      />
      <div v-else class="max-h-80 space-y-2 overflow-y-auto pr-1">
        <BaseCheckbox
          v-for="permission in permissions"
          :id="`permission-${permission.code}`"
          :key="permission.code"
          :model-value="selectedPermissions.includes(permission.code)"
          :name="permission.code"
          :label="permissionLabel(permission.code)"
          :description="permissionDescription(permission.code)"
          class="border border-[var(--color-border)] p-3"
          @update:model-value="updateSelectedPermission(permission.code, $event)"
        />
      </div>
      <div class="mt-5 flex justify-end gap-3">
        <BaseButton variant="secondary" @click="permissionsOpen = false">Hủy</BaseButton
        ><BaseButton :loading="permissionLoading" @click="savePermissions">Lưu quyền</BaseButton>
      </div>
    </AppModal>
  </AdminLayout>
</template>
