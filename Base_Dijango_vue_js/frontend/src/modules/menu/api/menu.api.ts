import { authClient } from "@/lib/http/client";
import type { MenuItem } from "../types/menu.types";
export async function menuRequest() {
  return (await authClient.get<MenuItem[]>("/api/v1/menu/")).data;
}
export async function validateCustomizationRequest(
  slug: string,
  input: {
    variant_id: number;
    topping_ids: number[];
    sweetness: string;
    ice: string;
    quantity: number;
  },
) {
  return (
    await authClient.post<{ unit_price: string; total_price: string }>(
      `/api/v1/menu/${slug}/validate-customization/`,
      input,
    )
  ).data;
}
