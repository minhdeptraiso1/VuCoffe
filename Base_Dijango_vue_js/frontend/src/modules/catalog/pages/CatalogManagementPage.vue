<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue";
import { Image as ImageIcon, Plus } from "lucide-vue-next";
import { useToastStore } from "@/app/stores/toast";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseCheckbox from "@/components/base/BaseCheckbox.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import BaseTextarea from "@/components/base/BaseTextarea.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import AppFileUpload from "@/components/files/AppFileUpload.vue";
import AppModal from "@/components/overlay/AppModal.vue";
import FormField from "@/components/form/FormField.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";
import { toAppError } from "@/lib/http/errors";
import {
  catalogCreate,
  catalogDeactivate,
  catalogList,
  catalogUploadProductImage,
  catalogUpdate,
  type CatalogRecord,
} from "../api/catalog.api";
const resources = [
  { id: "categories", label: "Danh mục" },
  { id: "products", label: "Món bán" },
  { id: "variants", label: "Kích cỡ & giá" },
  { id: "toppings", label: "Món thêm" },
];
const toast = useToastStore();
const active = ref("categories");
const rows = ref<CatalogRecord[]>([]);
const categories = ref<CatalogRecord[]>([]);
const products = ref<CatalogRecord[]>([]);
const loading = ref(false);
const error = ref("");
const open = ref(false);
const saving = ref(false);
const editing = ref<CatalogRecord | null>(null);
const imageFile = ref<File | null>(null);
const imagePreview = ref("");
const form = reactive({
  code: "",
  name: "",
  category: "",
  product: "",
  price: "0",
  slug: "",
  image_url: "",
  description: "",
  is_featured: false,
  is_active: true,
  no_stock_required: true,
});
const title = computed(
  () => resources.find((item) => item.id === active.value)?.label ?? "Dữ liệu",
);
async function load() {
  loading.value = true;
  error.value = "";
  try {
    [rows.value, categories.value, products.value] = await Promise.all([
      catalogList(active.value),
      catalogList("categories"),
      catalogList("products"),
    ]);
  } catch (reason) {
    error.value = toAppError(reason).message;
  } finally {
    loading.value = false;
  }
}
function reset() {
  clearImageSelection();
  Object.assign(form, {
    code: "",
    name: "",
    category: "",
    product: "",
    price: "0",
    slug: "",
    image_url: "",
    description: "",
    is_featured: false,
    is_active: true,
    no_stock_required: true,
  });
}
function clearImageSelection() {
  if (imagePreview.value.startsWith("blob:")) URL.revokeObjectURL(imagePreview.value);
  imageFile.value = null;
  imagePreview.value = "";
}
function selectImage(file: File | null) {
  clearImageSelection();
  imageFile.value = file;
  if (file) imagePreview.value = URL.createObjectURL(file);
}
function add() {
  editing.value = null;
  reset();
  open.value = true;
}
function edit(row: CatalogRecord) {
  editing.value = row;
  clearImageSelection();
  Object.assign(form, {
    code: row.code,
    name: row.name,
    category: String(row.category ?? ""),
    product: String(row.product ?? ""),
    price: row.price ?? "0",
    slug: row.slug ?? "",
    image_url: row.image_url ?? "",
    description: row.description ?? "",
    is_featured: Boolean(row.is_featured),
    is_active: row.is_active,
    no_stock_required: Boolean(row.no_stock_required),
  });
  open.value = true;
}
function payload() {
  const common: Record<string, unknown> = {
    code: form.code,
    name: form.name,
    is_active: form.is_active,
  };
  if (editing.value) common.version = editing.value.version;
  if (active.value === "products")
    Object.assign(common, {
      slug: form.slug || form.code,
      category: Number(form.category),
      description: form.description,
      image_url: form.image_url,
      is_featured: form.is_featured,
    });
  if (active.value === "variants")
    Object.assign(common, {
      product: Number(form.product),
      price: form.price,
      no_stock_required: form.no_stock_required,
    });
  if (active.value === "toppings")
    Object.assign(common, { price: form.price, no_stock_required: form.no_stock_required });
  return common;
}
async function save() {
  saving.value = true;
  try {
    if (active.value === "products" && imageFile.value) {
      const uploaded = await catalogUploadProductImage(imageFile.value);
      form.image_url = uploaded.image_url;
    }
    if (editing.value) await catalogUpdate(active.value, editing.value.id, payload());
    else await catalogCreate(active.value, payload());
    open.value = false;
    clearImageSelection();
    toast.show("Đã lưu dữ liệu thực đơn.", "success");
    await load();
  } catch (reason) {
    toast.show(toAppError(reason).message, "error");
  } finally {
    saving.value = false;
  }
}
async function deactivate(row: CatalogRecord) {
  try {
    await catalogDeactivate(active.value, row.id);
    toast.show("Đã ngừng sử dụng mục này.", "success");
    await load();
  } catch (reason) {
    toast.show(toAppError(reason).message, "error");
  }
}
async function switchTab(id: string) {
  active.value = id;
  await load();
}
onMounted(() => void load());
onBeforeUnmount(clearImageSelection);
</script>
<template>
  <AdminLayout
    ><div class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <p class="text-xs font-bold uppercase tracking-[.18em] text-[var(--color-primary)]">
          Phase 2 · Danh mục bán hàng
        </p>
        <h1 class="mt-1 font-[var(--font-display)] text-4xl font-bold">Quản lý thực đơn</h1>
        <p class="mt-2 text-[var(--color-text-muted)]">
          Quản lý danh mục, món, kích cỡ, giá và món thêm từ một nơi.
        </p>
      </div>
      <BaseButton @click="add"><Plus class="size-4" />Thêm {{ title.toLowerCase() }}</BaseButton>
    </div>
    <div class="mt-6 flex gap-2 overflow-x-auto">
      <BaseButton
        v-for="resource in resources"
        :key="resource.id"
        size="sm"
        :variant="active === resource.id ? 'primary' : 'secondary'"
        @click="switchTab(resource.id)"
        >{{ resource.label }}</BaseButton
      >
    </div>
    <AppAlert v-if="error" class="mt-5" variant="error" title="Chưa tải được dữ liệu">{{
      error
    }}</AppAlert>
    <section
      class="mt-5 overflow-hidden rounded-[var(--radius-lg)] border border-[var(--color-border)] bg-[var(--color-surface)]"
    >
      <div v-if="loading" class="p-8 text-center">Đang tải…</div>
      <div v-else-if="!rows.length" class="p-8 text-center text-[var(--color-text-muted)]">
        Chưa có dữ liệu.
      </div>
      <article
        v-for="row in rows"
        v-else
        :key="row.id"
        class="flex flex-wrap items-center justify-between gap-4 border-b border-[var(--color-border)] p-4 last:border-0"
      >
        <div>
          <h2 class="font-semibold">{{ row.name }}</h2>
          <p class="text-sm text-[var(--color-text-muted)]">
            {{ row.code
            }}<span v-if="row.price">
              · {{ new Intl.NumberFormat("vi-VN").format(Number(row.price)) }}đ</span
            >
          </p>
        </div>
        <div class="flex gap-2">
          <BaseButton size="sm" variant="secondary" @click="edit(row)">Chỉnh sửa</BaseButton
          ><BaseButton v-if="row.is_active" size="sm" variant="ghost" @click="deactivate(row)"
            >Ngừng dùng</BaseButton
          >
        </div>
      </article>
    </section>
    <AppModal
      :open="open"
      :title="editing ? `Chỉnh sửa ${title.toLowerCase()}` : `Thêm ${title.toLowerCase()}`"
      @close="open = false"
      ><form class="space-y-4" @submit.prevent="save">
        <FormField label="Mã" for-id="catalog-code"
          ><BaseInput
            id="catalog-code"
            v-model="form.code"
            name="code"
            placeholder="Ví dụ: ca-phe-dua"
            :disabled="Boolean(editing)"
            required /></FormField
        ><FormField label="Tên" for-id="catalog-name"
          ><BaseInput
            id="catalog-name"
            v-model="form.name"
            name="name"
            placeholder="Ví dụ: Cà phê dừa Kim Thành"
            required /></FormField
        ><template v-if="active === 'products'"
          ><FormField label="Danh mục" for-id="catalog-category"
            ><BaseSelect
              id="catalog-category"
              v-model="form.category"
              name="category"
              :options="
                categories.map((item) => ({ value: String(item.id), label: item.name }))
              " /></FormField
          ><FormField
            label="Đường dẫn"
            for-id="catalog-slug"
            help="Dùng chữ thường, không dấu và ngăn cách bằng dấu gạch ngang."
            ><BaseInput
              id="catalog-slug"
              v-model="form.slug"
              name="slug"
              placeholder="Ví dụ: ca-phe-dua-kim-thanh" /></FormField
          ><FormField
            label="Mô tả"
            for-id="catalog-description"
            help="Mô tả ngắn hương vị hoặc thành phần nổi bật của món."
            ><BaseTextarea
              id="catalog-description"
              v-model="form.description"
              name="description"
              :rows="3"
              placeholder="Ví dụ: Cà phê rang mộc hòa cùng cốt dừa béo nhẹ và lớp kem mịn." /></FormField
          ><FormField
            label="Ảnh món"
            for-id="catalog-image"
            help="Chọn ảnh ngang hoặc vuông, định dạng JPG, PNG, WEBP; tối đa 5 MB."
          >
            <div class="grid gap-3 sm:grid-cols-[8rem_minmax(0,1fr)] sm:items-stretch">
              <div
                class="flex aspect-square items-center justify-center overflow-hidden rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-surface-subtle)]"
              >
                <img
                  v-if="imagePreview || form.image_url"
                  :src="imagePreview || form.image_url"
                  alt="Xem trước ảnh món"
                  class="size-full object-cover"
                />
                <ImageIcon
                  v-else
                  class="size-8 text-[var(--color-text-muted)]"
                  aria-hidden="true"
                />
              </div>
              <AppFileUpload
                id="catalog-image"
                label="Chọn ảnh từ máy"
                accept="image/jpeg,image/png,image/webp"
                :max-size-mb="5"
                :disabled="saving"
                @select="selectImage"
              />
            </div> </FormField
          ><BaseCheckbox
            id="featured"
            v-model="form.is_featured"
            name="featured"
            label="Món nổi bật" /></template
        ><FormField v-if="active === 'variants'" label="Món" for-id="catalog-product"
          ><BaseSelect
            id="catalog-product"
            v-model="form.product"
            name="product"
            :options="
              products.map((item) => ({ value: String(item.id), label: item.name }))
            " /></FormField
        ><FormField
          v-if="['variants', 'toppings'].includes(active)"
          label="Giá bán"
          for-id="catalog-price"
          ><BaseInput
            id="catalog-price"
            v-model="form.price"
            name="price"
            type="number" /></FormField
        ><BaseCheckbox
          id="active"
          v-model="form.is_active"
          name="active"
          label="Đang sử dụng"
        /><BaseButton type="submit" block :loading="saving">Lưu dữ liệu</BaseButton>
      </form></AppModal
    ></AdminLayout
  >
</template>
