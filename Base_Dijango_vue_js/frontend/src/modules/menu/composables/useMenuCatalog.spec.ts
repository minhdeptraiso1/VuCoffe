import { vi } from "vitest";
import { menuPrice, useMenuCatalog } from "./useMenuCatalog";

const items = [
  {
    id: 1,
    code: "coffee",
    slug: "coffee",
    category: { id: 1, code: "coffee", name: "Cà phê", description: "" },
    name: "Cà phê muối",
    description: "Kem muối",
    image_url: "",
    image_position: "center",
    tag: "",
    is_featured: true,
    is_best_seller: true,
    is_new: false,
    variants: [
      { id: 1, code: "coffee-m", name: "M", volume_ml: 500, price: "32000.00", is_default: true },
    ],
    toppings: [],
    sweetness_options: [],
    ice_options: [],
  },
  {
    id: 2,
    code: "tea",
    slug: "tea",
    category: { id: 2, code: "tea", name: "Trà", description: "" },
    name: "Trà đào",
    description: "Thanh mát",
    image_url: "",
    image_position: "center",
    tag: "",
    is_featured: false,
    is_best_seller: false,
    is_new: true,
    variants: [
      { id: 2, code: "tea-m", name: "M", volume_ml: 500, price: "42000.00", is_default: true },
    ],
    toppings: [],
    sweetness_options: [],
    ice_options: [],
  },
];
vi.mock("../api/menu.api", () => ({ menuRequest: vi.fn(() => Promise.resolve(items)) }));

describe("useMenuCatalog", () => {
  it("loads, searches and resets menu data", async () => {
    const catalog = useMenuCatalog();
    await catalog.load();
    catalog.searchQuery.value = "muối";
    expect(catalog.filteredItems.value.map((item) => item.name)).toEqual(["Cà phê muối"]);
    catalog.resetFilters();
    expect(catalog.filteredItems.value).toHaveLength(2);
  });
  it("applies price filters and sorting", async () => {
    const catalog = useMenuCatalog();
    await catalog.load();
    catalog.selectedQuickFilter.value = "under35";
    expect(catalog.filteredItems.value.every((item) => menuPrice(item) < 35000)).toBe(true);
  });
});
