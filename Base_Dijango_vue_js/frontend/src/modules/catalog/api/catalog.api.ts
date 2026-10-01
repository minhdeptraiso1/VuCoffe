import { apiClient } from "@/lib/http/client";
export interface CatalogRecord {
  id: number;
  code: string;
  name: string;
  version: number;
  is_active: boolean;
  category?: number;
  product?: number;
  price?: string;
  slug?: string;
  image_url?: string;
  description?: string;
  is_featured?: boolean;
  no_stock_required?: boolean;
  [key: string]: unknown;
}
interface Page<T> {
  results: T[];
}
export async function catalogList(resource: string) {
  const data = (await apiClient.get<Page<CatalogRecord> | CatalogRecord[]>(`/api/v1/${resource}/`))
    .data;
  return Array.isArray(data) ? data : data.results;
}
export async function catalogCreate(resource: string, payload: Record<string, unknown>) {
  return (await apiClient.post<CatalogRecord>(`/api/v1/${resource}/`, payload)).data;
}
export async function catalogUpdate(
  resource: string,
  id: number,
  payload: Record<string, unknown>,
) {
  return (await apiClient.patch<CatalogRecord>(`/api/v1/${resource}/${String(id)}/`, payload)).data;
}
export async function catalogDeactivate(resource: string, id: number) {
  return (await apiClient.post<CatalogRecord>(`/api/v1/${resource}/${String(id)}/deactivate/`))
    .data;
}
export async function catalogUploadProductImage(file: File) {
  const body = new FormData();
  body.append("file", file);
  return (await apiClient.post<{ image_url: string }>("/api/v1/products/upload-image/", body)).data;
}
