export interface MenuCategory {
  id: number;
  code: string;
  name: string;
  description: string;
}
export interface MenuVariant {
  id: number;
  code: string;
  name: string;
  volume_ml: number | null;
  price: string;
  is_default: boolean;
}
export interface MenuTopping {
  id: number;
  code: string;
  name: string;
  price: string;
}
export interface MenuItem {
  id: number;
  code: string;
  slug: string;
  category: MenuCategory;
  name: string;
  description: string;
  image_url: string;
  image_position: string;
  tag: string;
  is_featured: boolean;
  is_best_seller: boolean;
  is_new: boolean;
  variants: MenuVariant[];
  toppings: MenuTopping[];
  sweetness_options: string[];
  ice_options: string[];
}
export type MenuSort = "popular" | "price-asc" | "price-desc";
export type MenuQuickFilter = "all" | "bestseller" | "new" | "under35";
export interface CustomizedOrderItem {
  item: MenuItem;
  size: string;
  sweetness: string;
  ice: string;
  toppings: string[];
  note: string;
  quantity: number;
  finalPrice: number;
}
export interface CartItem extends CustomizedOrderItem {
  id: string;
}
