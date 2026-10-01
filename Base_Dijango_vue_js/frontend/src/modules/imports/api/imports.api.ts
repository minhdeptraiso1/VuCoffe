import { apiClient } from "@/lib/http/client";
export interface ImportJob {
  id: number;
  module: string;
  mode: string;
  status: string;
  original_name: string;
  total_rows: number;
  new_rows: number;
  update_rows: number;
  error_rows: number;
  preview: Array<Record<string, unknown>>;
  issues: Array<{ row_number: number; column: string; message: string }>;
  created_at: string;
}
interface Page<T> {
  results: T[];
}
export async function importsRequest() {
  const data = (await apiClient.get<Page<ImportJob> | ImportJob[]>("/api/v1/imports/")).data;
  return Array.isArray(data) ? data : data.results;
}
export async function uploadImportRequest(module: string, mode: string, file: File) {
  const body = new FormData();
  body.append("module", module);
  body.append("mode", mode);
  body.append("file", file);
  return (await apiClient.post<ImportJob>("/api/v1/imports/", body)).data;
}
export async function confirmImportRequest(id: number) {
  return (
    await apiClient.post<ImportJob>(`/api/v1/imports/${String(id)}/confirm/`, {
      idempotency_key: `${String(id)}-${String(Date.now())}`,
    })
  ).data;
}
export async function downloadWorkbook(kind: "imports/templates" | "exports", module: string) {
  return (await apiClient.get<Blob>(`/api/v1/${kind}/${module}/`, { responseType: "blob" })).data;
}
export async function downloadErrorWorkbook(id: number) {
  return (
    await apiClient.get<Blob>(`/api/v1/imports/${String(id)}/error-file/`, { responseType: "blob" })
  ).data;
}
