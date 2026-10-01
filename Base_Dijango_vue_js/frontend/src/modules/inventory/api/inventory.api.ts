import { apiClient } from "@/lib/http/client";
export interface InventoryRecord {
  id: number;
  code?: string;
  name?: string;
  version?: number;
  is_active?: boolean;
  target_name?: string;
  product?: number;
  product_name?: string;
  variants?: InventoryRecord[];
  items?: Array<{
    ingredient: number;
    ingredient_name: string;
    unit_symbol: string;
    quantity: string;
  }>;
  symbol?: string;
  base_unit?: number;
  from_unit?: number;
  to_unit?: number;
  factor?: string;
  minimum_level?: string;
  contact_name?: string;
  phone?: string;
  email?: string;
  address?: string;
  [key: string]: unknown;
}
interface Page<T> {
  results: T[];
  next: string | null;
}
async function inventoryPage(url: string): Promise<Page<InventoryRecord> | InventoryRecord[]> {
  return (await apiClient.get<Page<InventoryRecord> | InventoryRecord[]>(url)).data;
}
export async function inventoryList(resource: string) {
  let url: string | null = `/api/v1/${resource}/`;
  const records: InventoryRecord[] = [];
  while (url) {
    const data = await inventoryPage(url);
    if (Array.isArray(data)) return [...records, ...data];
    records.push(...data.results);
    if (!data.next) break;
    url = data.next.replace(/^https?:\/\/[^/]+/u, "");
  }
  return records;
}
export async function inventoryCreate(resource: string, payload: Record<string, unknown>) {
  return (await apiClient.post<InventoryRecord>(`/api/v1/${resource}/`, payload)).data;
}
export async function inventoryUpdate(
  resource: string,
  id: number,
  payload: Record<string, unknown>,
) {
  return (await apiClient.patch<InventoryRecord>(`/api/v1/${resource}/${String(id)}/`, payload))
    .data;
}
