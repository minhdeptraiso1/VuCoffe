<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import { Plus, Trash2 } from "lucide-vue-next";
import { useToastStore } from "@/app/stores/toast";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseCheckbox from "@/components/base/BaseCheckbox.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import FormField from "@/components/form/FormField.vue";
import AppModal from "@/components/overlay/AppModal.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";
import { toAppError } from "@/lib/http/errors";
import {
  inventoryCreate,
  inventoryList,
  inventoryUpdate,
  type InventoryRecord,
} from "../api/inventory.api";
const tabs = [
  { id: "units", label: "Đơn vị" },
  { id: "unit-conversions", label: "Quy đổi đơn vị" },
  { id: "ingredients", label: "Nguyên liệu" },
  { id: "suppliers", label: "Nhà cung cấp" },
  { id: "recipes", label: "Công thức" },
];
const toast = useToastStore();
const active = ref("units");
const rows = ref<InventoryRecord[]>([]);
const units = ref<InventoryRecord[]>([]);
const variants = ref<InventoryRecord[]>([]);
const products = ref<InventoryRecord[]>([]);
const ingredients = ref<InventoryRecord[]>([]);
const loading = ref(false);
const error = ref("");
const open = ref(false);
const saving = ref(false);
const editing = ref<InventoryRecord | null>(null);
const form = reactive({
  code: "",
  name: "",
  symbol: "",
  from_unit: "",
  to_unit: "",
  factor: "1",
  base_unit: "",
  minimum_level: "0",
  contact_name: "",
  phone: "",
  email: "",
  address: "",
  product: "",
  variant: "",
  items: [{ ingredient: "", quantity: "1" }],
  is_active: true,
});
async function load() {
  loading.value = true;
  error.value = "";
  try {
    [rows.value, units.value, variants.value, products.value, ingredients.value] =
      await Promise.all([
        inventoryList(active.value),
        inventoryList("units"),
        inventoryList("variants"),
        inventoryList("products"),
        inventoryList("ingredients"),
      ]);
  } catch (reason) {
    error.value = toAppError(reason).message;
  } finally {
    loading.value = false;
  }
}
function add() {
  editing.value = null;
  Object.assign(form, {
    code: "",
    name: "",
    symbol: "",
    from_unit: "",
    to_unit: "",
    factor: "1",
    base_unit: "",
    minimum_level: "0",
    contact_name: "",
    phone: "",
    email: "",
    address: "",
    product: "",
    variant: "",
    items: [{ ingredient: "", quantity: "1" }],
    is_active: true,
  });
  open.value = true;
}
const activeTabLabel = computed(
  () => tabs.find((tab) => tab.id === active.value)?.label ?? "dữ liệu",
);
const actionLabel = computed(() =>
  active.value === "recipes" ? "Tạo công thức" : `Thêm ${activeTabLabel.value.toLowerCase()}`,
);
const productVariants = computed(() =>
  variants.value.filter((variant) => String(variant.product ?? "") === form.product),
);
const recipeValid = computed(
  () =>
    Boolean(form.product && form.variant) &&
    form.items.length > 0 &&
    form.items.every((item) => Boolean(item.ingredient) && Number(item.quantity) > 0),
);
const conversionValid = computed(
  () =>
    Boolean(form.from_unit && form.to_unit) &&
    form.from_unit !== form.to_unit &&
    Number(form.factor) > 0,
);
function addRecipeItem() {
  form.items.push({ ingredient: "", quantity: "1" });
}
function removeRecipeItem(index: number) {
  if (form.items.length > 1) form.items.splice(index, 1);
}
function ingredientUnit(ingredientId: string) {
  const ingredient = ingredients.value.find((item) => String(item.id) === ingredientId);
  const unit = units.value.find((item) => item.id === Number(ingredient?.base_unit));
  return unit?.symbol ?? "đơn vị";
}
function unitLabel(unitId: unknown) {
  const unit = units.value.find((item) => item.id === Number(unitId));
  return unit ? `${String(unit.name)} (${String(unit.symbol)})` : "Đơn vị chưa xác định";
}
function rowTitle(row: InventoryRecord) {
  if (active.value === "unit-conversions") {
    return `${unitLabel(row.from_unit)} → ${unitLabel(row.to_unit)}`;
  }
  return row.name || row.target_name || "Dữ liệu chưa đặt tên";
}
function rowMeta(row: InventoryRecord) {
  if (active.value === "unit-conversions") return `Hệ số quy đổi: ${String(row.factor)}`;
  if (active.value === "recipes") {
    return `Phiên bản ${String(row.version)} · ${String(row.items?.length ?? 0)} nguyên liệu`;
  }
  return row.code ?? "";
}
function edit(row: InventoryRecord) {
  editing.value = row;
  Object.assign(form, {
    code: row.code ?? "",
    name: row.name ?? "",
    symbol: row.symbol ?? "",
    from_unit: String(row.from_unit ?? ""),
    to_unit: String(row.to_unit ?? ""),
    factor: row.factor ?? "1",
    base_unit: String(row.base_unit ?? ""),
    minimum_level: row.minimum_level ?? "0",
    contact_name: row.contact_name ?? "",
    phone: row.phone ?? "",
    email: row.email ?? "",
    address: row.address ?? "",
    is_active: Boolean(row.is_active),
  });
  open.value = true;
}
function payload() {
  if (active.value === "units")
    return {
      code: form.code,
      name: form.name,
      symbol: form.symbol,
      decimal_places: 2,
      is_active: form.is_active,
      ...(editing.value ? { version: editing.value.version } : {}),
    };
  if (active.value === "unit-conversions")
    return {
      from_unit: Number(form.from_unit),
      to_unit: Number(form.to_unit),
      factor: form.factor,
    };
  if (active.value === "ingredients")
    return {
      code: form.code,
      name: form.name,
      base_unit: Number(form.base_unit),
      minimum_level: form.minimum_level,
      track_lot: false,
      is_active: form.is_active,
      ...(editing.value ? { version: editing.value.version } : {}),
    };
  if (active.value === "suppliers")
    return {
      code: form.code,
      name: form.name,
      contact_name: form.contact_name,
      phone: form.phone,
      email: form.email,
      address: form.address,
      is_active: form.is_active,
      ...(editing.value ? { version: editing.value.version } : {}),
    };
  return {
    variant: Number(form.variant),
    items: form.items.map((item) => ({
      ingredient: Number(item.ingredient),
      quantity: item.quantity,
    })),
  };
}
async function save() {
  saving.value = true;
  try {
    if (editing.value && active.value !== "recipes")
      await inventoryUpdate(active.value, editing.value.id, payload());
    else await inventoryCreate(active.value, payload());
    open.value = false;
    toast.show("Đã lưu dữ liệu vận hành.", "success");
    await load();
  } catch (reason) {
    toast.show(toAppError(reason).message, "error");
  } finally {
    saving.value = false;
  }
}
async function switchTab(id: string) {
  active.value = id;
  await load();
}
watch(
  () => form.product,
  () => {
    if (!productVariants.value.some((variant) => String(variant.id) === form.variant)) {
      form.variant = "";
    }
  },
);
onMounted(() => void load());
</script>
<template>
  <AdminLayout
    ><div class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <p class="text-xs font-bold uppercase tracking-[.18em] text-[var(--color-primary)]">
          Phase 2 · Dữ liệu vận hành
        </p>
        <h1 class="mt-1 font-[var(--font-display)] text-4xl font-bold">Nguyên liệu & công thức</h1>
        <p class="mt-2 text-[var(--color-text-muted)]">
          Chuẩn hóa đơn vị, nguyên liệu, nhà cung cấp và định lượng pha chế.
        </p>
      </div>
      <BaseButton @click="add"><Plus class="size-4" />{{ actionLabel }}</BaseButton>
    </div>
    <div class="mt-6 flex gap-2 overflow-x-auto">
      <BaseButton
        v-for="tab in tabs"
        :key="tab.id"
        size="sm"
        :variant="active === tab.id ? 'primary' : 'secondary'"
        @click="switchTab(tab.id)"
        >{{ tab.label }}</BaseButton
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
        class="flex items-center justify-between gap-4 border-b border-[var(--color-border)] p-4 last:border-0"
      >
        <div class="min-w-0">
          <h2 class="font-semibold">{{ rowTitle(row) }}</h2>
          <p class="text-sm text-[var(--color-text-muted)]">
            {{ rowMeta(row) }}
          </p>
          <ul v-if="active === 'recipes'" class="mt-2 flex flex-wrap gap-2 text-xs">
            <li
              v-for="item in row.items"
              :key="item.ingredient"
              class="rounded-full bg-[var(--color-primary-soft)] px-2.5 py-1 text-[var(--color-primary)]"
            >
              {{ item.ingredient_name }} · {{ item.quantity }} {{ item.unit_symbol }}
            </li>
          </ul>
        </div>
        <BaseButton v-if="active !== 'recipes'" size="sm" variant="secondary" @click="edit(row)"
          >Chỉnh sửa</BaseButton
        >
      </article>
    </section>
    <AppModal
      :open="open"
      :title="
        active === 'recipes'
          ? 'Tạo công thức pha chế'
          : editing
            ? `Chỉnh sửa ${activeTabLabel.toLowerCase()}`
            : actionLabel
      "
      @close="open = false"
      ><form class="space-y-4" @submit.prevent="save">
        <template v-if="!['recipes', 'unit-conversions'].includes(active)"
          ><FormField label="Mã" for-id="master-code"
            ><BaseInput
              id="master-code"
              v-model="form.code"
              name="code"
              :disabled="Boolean(editing)"
              required /></FormField
          ><FormField label="Tên" for-id="master-name"
            ><BaseInput
              id="master-name"
              v-model="form.name"
              name="name"
              required /></FormField></template
        ><FormField v-if="active === 'units'" label="Ký hiệu" for-id="unit-symbol"
          ><BaseInput id="unit-symbol" v-model="form.symbol" name="symbol" required /></FormField
        ><template v-if="active === 'unit-conversions'">
          <div class="rounded-[var(--radius-md)] bg-[var(--color-primary-soft)] p-4 text-sm">
            Khai báo cách quy đổi theo công thức: 1 đơn vị nguồn bằng hệ số × đơn vị đích.
          </div>
          <div class="grid gap-4 sm:grid-cols-2">
            <FormField label="Đơn vị nguồn" for-id="conversion-from" required>
              <BaseSelect
                id="conversion-from"
                v-model="form.from_unit"
                name="from_unit"
                :options="
                  units.map((item) => ({
                    value: String(item.id),
                    label: `${String(item.name)} (${String(item.symbol)})`,
                    disabled: String(item.id) === form.to_unit,
                  }))
                "
                required
              />
            </FormField>
            <FormField label="Đơn vị đích" for-id="conversion-to" required>
              <BaseSelect
                id="conversion-to"
                v-model="form.to_unit"
                name="to_unit"
                :options="
                  units.map((item) => ({
                    value: String(item.id),
                    label: `${String(item.name)} (${String(item.symbol)})`,
                    disabled: String(item.id) === form.from_unit,
                  }))
                "
                required
              />
            </FormField>
          </div>
          <FormField
            label="Hệ số quy đổi"
            for-id="conversion-factor"
            help="Ví dụ: 1 kg = 1.000 g thì nhập 1000."
            required
          >
            <BaseInput
              id="conversion-factor"
              v-model="form.factor"
              name="factor"
              type="number"
              min="0.00000001"
              step="0.00000001"
              required
            />
          </FormField> </template
        ><template v-if="active === 'ingredients'"
          ><FormField label="Đơn vị cơ sở" for-id="base-unit"
            ><BaseSelect
              id="base-unit"
              v-model="form.base_unit"
              name="base_unit"
              :options="
                units.map((item) => ({
                  value: String(item.id),
                  label: `${item.name} (${item.symbol})`,
                }))
              " /></FormField
          ><FormField label="Mức tồn tối thiểu" for-id="minimum"
            ><BaseInput
              id="minimum"
              v-model="form.minimum_level"
              name="minimum"
              type="number" /></FormField></template
        ><template v-if="active === 'suppliers'"
          ><FormField label="Người liên hệ" for-id="contact"
            ><BaseInput id="contact" v-model="form.contact_name" name="contact" /></FormField
          ><FormField label="Điện thoại" for-id="phone"
            ><BaseInput id="phone" v-model="form.phone" name="phone" /></FormField
          ><FormField label="Email" for-id="email"
            ><BaseInput id="email" v-model="form.email" name="email" /></FormField
          ><FormField label="Địa chỉ" for-id="address"
            ><BaseInput id="address" v-model="form.address" name="address" /></FormField></template
        ><template v-if="active === 'recipes'">
          <div class="rounded-[var(--radius-md)] bg-[var(--color-primary-soft)] p-4 text-sm">
            Chọn món và kích cỡ trước, sau đó khai báo từng nguyên liệu. Khi lưu, phiên bản công
            thức cũ sẽ được giữ lại trong lịch sử.
          </div>
          <div class="grid gap-4 sm:grid-cols-2">
            <FormField label="Món bán" for-id="recipe-product" required>
              <BaseSelect
                id="recipe-product"
                v-model="form.product"
                name="product"
                placeholder="Chọn món cần tạo công thức"
                :options="
                  products.map((item) => ({ value: String(item.id), label: String(item.name) }))
                "
                required
              />
            </FormField>
            <FormField
              label="Kích cỡ / biến thể"
              for-id="recipe-variant"
              required
              :help="form.product ? '' : 'Chọn món trước để xem các kích cỡ.'"
            >
              <BaseSelect
                id="recipe-variant"
                v-model="form.variant"
                name="variant"
                placeholder="Chọn kích cỡ"
                :disabled="!form.product"
                :options="
                  productVariants.map((item) => ({
                    value: String(item.id),
                    label: String(item.name),
                  }))
                "
                required
              />
            </FormField>
          </div>
          <div class="space-y-3">
            <div class="flex items-center justify-between gap-3">
              <div>
                <h3 class="font-semibold">Định lượng nguyên liệu</h3>
                <p class="text-sm text-[var(--color-text-muted)]">
                  Đơn vị được lấy tự động từ hồ sơ nguyên liệu.
                </p>
              </div>
              <BaseButton type="button" size="sm" variant="secondary" @click="addRecipeItem">
                <Plus class="size-4" /> Thêm nguyên liệu
              </BaseButton>
            </div>
            <div
              v-for="(item, index) in form.items"
              :key="index"
              class="grid items-end gap-3 rounded-[var(--radius-md)] border border-[var(--color-border)] p-3 sm:grid-cols-[minmax(0,1fr)_9rem_auto]"
            >
              <FormField
                :label="`Nguyên liệu ${index + 1}`"
                :for-id="`recipe-ingredient-${index}`"
                required
              >
                <BaseSelect
                  :id="`recipe-ingredient-${index}`"
                  v-model="item.ingredient"
                  :name="`ingredient-${index}`"
                  placeholder="Chọn nguyên liệu"
                  :options="
                    ingredients.map((ingredient) => ({
                      value: String(ingredient.id),
                      label: String(ingredient.name),
                      disabled: form.items.some(
                        (selected, selectedIndex) =>
                          selectedIndex !== index && selected.ingredient === String(ingredient.id),
                      ),
                    }))
                  "
                  required
                />
              </FormField>
              <FormField
                :label="`Số lượng (${ingredientUnit(item.ingredient)})`"
                :for-id="`recipe-quantity-${index}`"
                required
              >
                <BaseInput
                  :id="`recipe-quantity-${index}`"
                  v-model="item.quantity"
                  :name="`quantity-${index}`"
                  type="number"
                  min="0.001"
                  step="0.001"
                  required
                />
              </FormField>
              <BaseButton
                type="button"
                size="sm"
                variant="ghost"
                :disabled="form.items.length === 1"
                :aria-label="`Xóa nguyên liệu ${index + 1}`"
                @click="removeRecipeItem(index)"
              >
                <Trash2 class="size-4" />
              </BaseButton>
            </div>
          </div> </template
        ><BaseCheckbox
          v-if="!['recipes', 'unit-conversions'].includes(active)"
          id="master-active"
          v-model="form.is_active"
          name="active"
          label="Đang sử dụng"
        /><BaseButton
          type="submit"
          block
          :loading="saving"
          :disabled="
            (active === 'recipes' && !recipeValid) ||
            (active === 'unit-conversions' && !conversionValid)
          "
          >{{ active === "recipes" ? "Lưu công thức" : "Lưu dữ liệu" }}</BaseButton
        >
      </form></AppModal
    ></AdminLayout
  >
</template>
