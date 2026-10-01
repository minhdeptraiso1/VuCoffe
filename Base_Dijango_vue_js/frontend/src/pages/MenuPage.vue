<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ShoppingBag, X } from "lucide-vue-next";
import { useToastStore } from "@/app/stores/toast";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import AppEmptyState from "@/components/feedback/AppEmptyState.vue";
import AppSkeleton from "@/components/feedback/AppSkeleton.vue";
import PublicHeader from "@/components/layout/PublicHeader.vue";
import MenuCartModal from "@/modules/menu/components/MenuCartModal.vue";
import MenuSection from "@/modules/menu/components/MenuSection.vue";
import ProductCustomizeModal from "@/modules/menu/components/ProductCustomizeModal.vue";
import { useMenuCart } from "@/modules/menu/composables/useMenuCart";
import { useMenuCatalog } from "@/modules/menu/composables/useMenuCatalog";
import type {
  CustomizedOrderItem,
  MenuItem,
  MenuQuickFilter,
} from "@/modules/menu/types/menu.types";
const quickFilters: Array<{ value: MenuQuickFilter; label: string }> = [
  { value: "all", label: "Tất cả món" },
  { value: "bestseller", label: "Món bán chạy" },
  { value: "new", label: "Món mới" },
  { value: "under35", label: "Dưới 35 nghìn" },
];
const sorts = [
  { value: "popular", label: "Phổ biến nhất" },
  { value: "price-asc", label: "Giá tăng dần" },
  { value: "price-desc", label: "Giá giảm dần" },
];
const toast = useToastStore();
const catalog = useMenuCatalog();
const cart = useMenuCart();
const selectedItem = ref<MenuItem | null>(null);
const customizeOpen = ref(false);
const cartOpen = ref(false);
const sections = computed(() =>
  catalog.categories.value
    .map((category) => ({
      ...category,
      items: catalog.filteredItems.value.filter((item) => item.category.code === category.code),
    }))
    .filter((section) => section.items.length),
);
function selectItem(item: MenuItem) {
  selectedItem.value = item;
  customizeOpen.value = true;
}
function addToCart(item: CustomizedOrderItem) {
  cart.addItem(item);
  toast.show(`Đã thêm “${item.item.name}” vào giỏ.`, "success");
}
onMounted(() => void catalog.load());
</script>
<template>
  <div class="min-h-screen bg-[var(--color-surface-subtle)] pb-24 text-[var(--color-text)] sm:pb-0">
    <PublicHeader :cart-count="cart.totalItems.value" @open-cart="cartOpen = true" />
    <main class="px-3 py-5 sm:px-6 sm:py-8">
      <article
        data-menu-sheet
        class="mx-auto max-w-6xl overflow-hidden border border-[var(--color-border)] bg-[var(--color-surface)] shadow-[var(--shadow-surface)]"
      >
        <header class="border-b border-[var(--color-border)] px-5 py-7 sm:px-10">
          <div class="grid items-end gap-6 lg:grid-cols-[1fr_.8fr]">
            <div>
              <p class="text-xs font-bold uppercase tracking-[.24em] text-[var(--color-accent)]">
                Kim Thành Coffee
              </p>
              <h1 class="mt-2 font-[var(--font-display)] text-4xl font-bold sm:text-5xl">
                Thực đơn
              </h1>
              <p class="mt-2 text-sm text-[var(--color-text-muted)]">
                Chọn món, tùy chỉnh khẩu vị và thêm vào giỏ trong vài bước.
              </p>
            </div>
            <div>
              <label for="menu-search" class="mb-1 block text-xs font-bold uppercase tracking-wider"
                >Tìm món</label
              >
              <div class="flex w-full items-center border-b border-[var(--color-primary)]">
                <div class="min-w-0 flex-1">
                  <BaseInput
                    id="menu-search"
                    v-model="catalog.searchQuery.value"
                    name="menu-search"
                    aria-label="Tìm món trong thực đơn"
                    class="border-0 bg-transparent px-0 shadow-none"
                    placeholder="Tên món hoặc hương vị…"
                  />
                </div>
                <BaseButton
                  v-if="catalog.searchQuery.value"
                  variant="text"
                  size="sm"
                  class="ml-2 shrink-0"
                  aria-label="Xóa tìm kiếm"
                  @click="catalog.searchQuery.value = ''"
                  ><X class="size-4"
                /></BaseButton>
              </div>
            </div>
          </div>
        </header>
        <nav
          class="flex gap-1 overflow-x-auto border-b border-[var(--color-border)] px-5 py-2 sm:px-10"
          aria-label="Danh mục món"
        >
          <BaseButton
            size="sm"
            :variant="catalog.selectedCategory.value === 'all' ? 'primary' : 'text'"
            @click="catalog.selectedCategory.value = 'all'"
            >Tất cả · {{ catalog.categoryCount("all") }}</BaseButton
          ><BaseButton
            v-for="category in catalog.categories.value"
            :key="category.code"
            size="sm"
            :variant="catalog.selectedCategory.value === category.code ? 'primary' : 'text'"
            class="shrink-0"
            @click="catalog.selectedCategory.value = category.code"
            >{{ category.name }} · {{ catalog.categoryCount(category.code) }}</BaseButton
          >
        </nav>
        <section
          class="grid gap-3 border-b border-[var(--color-border)] px-5 py-4 sm:grid-cols-2 sm:px-10"
        >
          <div>
            <label
              for="menu-filter"
              class="mb-1 block text-xs font-semibold text-[var(--color-text-muted)]"
              >Lọc món</label
            ><BaseSelect
              id="menu-filter"
              v-model="catalog.selectedQuickFilter.value"
              name="menu-filter"
              :options="quickFilters"
            />
          </div>
          <div>
            <label
              for="menu-sort"
              class="mb-1 block text-xs font-semibold text-[var(--color-text-muted)]"
              >Sắp xếp</label
            ><BaseSelect
              id="menu-sort"
              v-model="catalog.sortOption.value"
              name="menu-sort"
              :options="sorts"
            />
          </div>
        </section>
        <div class="px-5 py-8 sm:px-10">
          <AppAlert v-if="catalog.error.value" variant="error" title="Chưa tải được thực đơn"
            >{{ catalog.error.value }}
            <div class="mt-3">
              <BaseButton size="sm" variant="secondary" @click="catalog.load">Thử lại</BaseButton>
            </div></AppAlert
          >
          <div v-else-if="catalog.loading.value" class="grid gap-8 lg:grid-cols-2" role="status">
            <AppSkeleton v-for="index in 4" :key="index" class="h-72" />
          </div>
          <AppEmptyState
            v-else-if="!catalog.filteredItems.value.length"
            title="Không tìm thấy món phù hợp"
            description="Thử từ khóa ngắn hơn hoặc xóa bộ lọc."
            ><template #action
              ><BaseButton class="mt-4" @click="catalog.resetFilters"
                >Xem toàn bộ thực đơn</BaseButton
              ></template
            ></AppEmptyState
          >
          <div v-else class="grid gap-x-14 gap-y-12 lg:grid-cols-2">
            <MenuSection
              v-for="section in sections"
              :key="section.code"
              :title="section.name"
              :description="section.description"
              :items="section.items"
              @select="selectItem"
            />
          </div>
        </div>
      </article>
    </main>
    <div class="fixed inset-x-4 bottom-4 z-20 sm:hidden">
      <BaseButton block size="lg" class="justify-between" @click="cartOpen = true"
        ><span class="inline-flex items-center gap-2"
          ><ShoppingBag class="size-5" />Giỏ hàng · {{ cart.totalItems.value }}</span
        ><span>{{ new Intl.NumberFormat("vi-VN").format(cart.subtotal.value) }}đ</span></BaseButton
      >
    </div>
    <ProductCustomizeModal
      v-model="customizeOpen"
      :item="selectedItem"
      @add-to-cart="addToCart"
    /><MenuCartModal
      :open="cartOpen"
      :items="cart.items.value"
      :subtotal="cart.subtotal.value"
      @close="cartOpen = false"
      @remove="cart.removeItem"
    />
  </div>
</template>
