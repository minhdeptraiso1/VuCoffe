import { computed, ref } from "vue";
import { menuRequest } from "../api/menu.api";
import type { MenuItem, MenuQuickFilter, MenuSort } from "../types/menu.types";
export function menuPrice(item: MenuItem) {
  return Number(item.variants.find((v) => v.is_default)?.price ?? item.variants[0]?.price ?? 0);
}
export function useMenuCatalog() {
  const items = ref<MenuItem[]>([]);
  const loading = ref(false);
  const error = ref("");
  const searchQuery = ref("");
  const selectedCategory = ref("all");
  const selectedQuickFilter = ref<MenuQuickFilter>("all");
  const sortOption = ref<MenuSort>("popular");
  const categories = computed(() =>
    Array.from(new Map(items.value.map((item) => [item.category.code, item.category])).values()),
  );
  const filteredItems = computed(() => {
    const query = searchQuery.value.trim().toLocaleLowerCase("vi");
    return items.value
      .filter(
        (item) =>
          (!query || `${item.name} ${item.description}`.toLocaleLowerCase("vi").includes(query)) &&
          (selectedCategory.value === "all" || item.category.code === selectedCategory.value) &&
          (selectedQuickFilter.value === "all" ||
            (selectedQuickFilter.value === "bestseller" && item.is_best_seller) ||
            (selectedQuickFilter.value === "new" && item.is_new) ||
            (selectedQuickFilter.value === "under35" && menuPrice(item) < 35000)),
      )
      .sort((a, b) =>
        sortOption.value === "price-asc"
          ? menuPrice(a) - menuPrice(b)
          : sortOption.value === "price-desc"
            ? menuPrice(b) - menuPrice(a)
            : Number(b.is_best_seller) - Number(a.is_best_seller),
      );
  });
  const hasActiveFilters = computed(
    () =>
      Boolean(searchQuery.value.trim()) ||
      selectedCategory.value !== "all" ||
      selectedQuickFilter.value !== "all",
  );
  async function load() {
    loading.value = true;
    error.value = "";
    try {
      items.value = await menuRequest();
    } catch {
      error.value = "Chưa thể tải thực đơn. Vui lòng thử lại.";
    } finally {
      loading.value = false;
    }
  }
  function resetFilters() {
    searchQuery.value = "";
    selectedCategory.value = "all";
    selectedQuickFilter.value = "all";
    sortOption.value = "popular";
  }
  function categoryCount(code: string) {
    return code === "all"
      ? items.value.length
      : items.value.filter((item) => item.category.code === code).length;
  }
  return {
    items,
    loading,
    error,
    load,
    categories,
    searchQuery,
    selectedCategory,
    selectedQuickFilter,
    sortOption,
    filteredItems,
    hasActiveFilters,
    resetFilters,
    categoryCount,
  };
}
