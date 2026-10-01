<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useToastStore } from "@/app/stores/toast";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import AppFileUpload from "@/components/files/AppFileUpload.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";
import { toAppError } from "@/lib/http/errors";
import {
  confirmImportRequest,
  downloadErrorWorkbook,
  downloadWorkbook,
  importsRequest,
  uploadImportRequest,
  type ImportJob,
} from "../api/imports.api";
const modules = [
  { value: "categories", label: "Danh mục" },
  { value: "products", label: "Món bán" },
  { value: "ingredients", label: "Nguyên liệu" },
  { value: "suppliers", label: "Nhà cung cấp" },
];
const modes = [
  { value: "upsert", label: "Thêm mới và cập nhật" },
  { value: "create", label: "Chỉ thêm mới" },
  { value: "update", label: "Chỉ cập nhật" },
];
const toast = useToastStore();
const module = ref("categories");
const mode = ref("upsert");
const file = ref<File | null>(null);
const jobs = ref<ImportJob[]>([]);
const preview = ref<ImportJob | null>(null);
const loading = ref(false);
const error = ref("");
async function load() {
  try {
    jobs.value = await importsRequest();
  } catch (reason) {
    error.value = toAppError(reason).message;
  }
}
async function upload() {
  if (!file.value) return;
  loading.value = true;
  error.value = "";
  try {
    preview.value = await uploadImportRequest(module.value, mode.value, file.value);
    toast.show("Đã kiểm tra file. Hãy xem kết quả trước khi xác nhận.", "success");
    await load();
  } catch (reason) {
    error.value = toAppError(reason).message;
    toast.show(error.value, "error");
  } finally {
    loading.value = false;
  }
}
async function confirm() {
  if (!preview.value) return;
  loading.value = true;
  try {
    preview.value = await confirmImportRequest(preview.value.id);
    toast.show("Đã nhập dữ liệu thành công.", "success");
    await load();
  } catch (reason) {
    toast.show(toAppError(reason).message, "error");
  } finally {
    loading.value = false;
  }
}
async function download(kind: "imports/templates" | "exports") {
  try {
    const blob = await downloadWorkbook(kind, module.value);
    const url = URL.createObjectURL(blob);
    const anchor = globalThis.document.createElement("a");
    anchor.href = url;
    anchor.download = `${module.value}-${kind === "exports" ? "export" : "template"}.xlsx`;
    anchor.click();
    URL.revokeObjectURL(url);
  } catch (reason) {
    toast.show(toAppError(reason).message, "error");
  }
}
async function downloadErrors() {
  if (!preview.value) return;
  try {
    const blob = await downloadErrorWorkbook(preview.value.id);
    const url = URL.createObjectURL(blob);
    const anchor = globalThis.document.createElement("a");
    anchor.href = url;
    anchor.download = `import-${String(preview.value.id)}-errors.xlsx`;
    anchor.click();
    URL.revokeObjectURL(url);
  } catch (reason) {
    toast.show(toAppError(reason).message, "error");
  }
}
onMounted(() => void load());
</script>
<template>
  <AdminLayout
    ><div>
      <p class="text-xs font-bold uppercase tracking-[.18em] text-[var(--color-primary)]">
        Phase 2 · Dữ liệu hàng loạt
      </p>
      <h1 class="mt-1 font-[var(--font-display)] text-4xl font-bold">Nhập & xuất Excel</h1>
      <p class="mt-2 text-[var(--color-text-muted)]">
        Tải file mẫu, kiểm tra lỗi, xem trước thay đổi rồi mới ghi dữ liệu.
      </p>
    </div>
    <div class="mt-6 grid gap-6 xl:grid-cols-[.85fr_1.15fr]">
      <section
        class="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
      >
        <h2 class="text-xl font-bold">Tạo lượt nhập dữ liệu</h2>
        <div
          class="mt-4 rounded-[var(--radius-md)] bg-[var(--color-primary-soft)] p-4 text-sm text-[var(--color-text)]"
        >
          <strong class="block">File mẫu đã sẵn sàng để nhập liệu</strong>
          <ul class="mt-2 list-disc space-y-1 pl-5 text-[var(--color-text-muted)]">
            <li>Tiêu đề có dấu (*) là trường bắt buộc.</li>
            <li>Danh mục, đơn vị và trường Có/Không có danh sách chọn từ hệ thống.</li>
            <li>Các ô mô tả, liên hệ và dữ liệu tự do có thể nhập trực tiếp.</li>
          </ul>
        </div>
        <div class="mt-4 space-y-4">
          <div>
            <label class="mb-1 block text-sm font-semibold" for="import-module">Loại dữ liệu</label
            ><BaseSelect id="import-module" v-model="module" name="module" :options="modules" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold" for="import-mode">Chế độ</label
            ><BaseSelect id="import-mode" v-model="mode" name="mode" :options="modes" />
          </div>
          <AppFileUpload id="import-file" label="Chọn file Excel" @select="file = $event" />
          <div class="grid gap-2 sm:grid-cols-3">
            <BaseButton variant="secondary" @click="download('imports/templates')"
              >Tải file mẫu</BaseButton
            ><BaseButton variant="secondary" @click="download('exports')">Xuất dữ liệu</BaseButton
            ><BaseButton :disabled="!file" :loading="loading" @click="upload"
              >Kiểm tra file</BaseButton
            >
          </div>
          <AppAlert v-if="error" variant="error" title="Chưa thể xử lý file">{{ error }}</AppAlert>
        </div>
      </section>
      <section
        class="rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
      >
        <h2 class="text-xl font-bold">Kết quả xem trước</h2>
        <p v-if="!preview" class="mt-4 text-sm text-[var(--color-text-muted)]">
          Chọn file để xem số dòng mới, cập nhật và lỗi trước khi xác nhận.
        </p>
        <template v-else
          ><div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div class="rounded bg-[var(--color-surface-subtle)] p-3">
              <strong class="block text-xl">{{ preview.total_rows }}</strong
              ><span class="text-xs">Tổng dòng</span>
            </div>
            <div class="rounded bg-[var(--color-success-soft)] p-3">
              <strong class="block text-xl">{{ preview.new_rows }}</strong
              ><span class="text-xs">Thêm mới</span>
            </div>
            <div class="rounded bg-[var(--color-primary-soft)] p-3">
              <strong class="block text-xl">{{ preview.update_rows }}</strong
              ><span class="text-xs">Cập nhật</span>
            </div>
            <div class="rounded bg-[var(--color-error-soft)] p-3">
              <strong class="block text-xl">{{ preview.error_rows }}</strong
              ><span class="text-xs">Có lỗi</span>
            </div>
          </div>
          <ul
            v-if="preview.issues.length"
            class="mt-4 max-h-48 overflow-auto text-sm text-[var(--color-error)]"
          >
            <li v-for="issue in preview.issues" :key="`${issue.row_number}-${issue.column}`">
              Dòng {{ issue.row_number }}, {{ issue.column }}: {{ issue.message }}
            </li>
          </ul>
          <BaseButton
            v-if="preview.issues.length"
            class="mt-5 mr-2"
            variant="secondary"
            @click="downloadErrors"
            >Tải file lỗi</BaseButton
          >
          <BaseButton
            v-if="preview.status === 'ready'"
            class="mt-5"
            :loading="loading"
            @click="confirm"
            >Xác nhận nhập dữ liệu</BaseButton
          ></template
        >
      </section>
    </div>
    <section
      class="mt-6 rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)] p-5"
    >
      <h2 class="text-xl font-bold">Lịch sử xử lý</h2>
      <div class="mt-4 divide-y divide-[var(--color-border)]">
        <article
          v-for="job in jobs"
          :key="job.id"
          class="flex flex-wrap justify-between gap-3 py-3"
        >
          <div>
            <strong>{{ job.original_name }}</strong>
            <p class="text-sm text-[var(--color-text-muted)]">
              {{ job.module }} · {{ new Date(job.created_at).toLocaleString("vi-VN") }}
            </p>
          </div>
          <span class="text-sm font-semibold">{{ job.status }} · {{ job.total_rows }} dòng</span>
        </article>
        <p v-if="!jobs.length" class="py-4 text-sm text-[var(--color-text-muted)]">
          Chưa có lịch sử nhập dữ liệu.
        </p>
      </div>
    </section></AdminLayout
  >
</template>
