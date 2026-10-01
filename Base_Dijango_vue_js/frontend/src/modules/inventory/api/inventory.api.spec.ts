import { vi } from "vitest";

const client = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn(), patch: vi.fn() }));
vi.mock("@/lib/http/client", () => ({ apiClient: client }));

import { inventoryList } from "./inventory.api";

describe("inventory API", () => {
  it("loads every page needed by the recipe builder", async () => {
    client.get
      .mockResolvedValueOnce({
        data: {
          results: [{ id: 1, name: "Cà phê muối" }],
          next: "http://api.test/api/v1/products/?page=2",
        },
      })
      .mockResolvedValueOnce({
        data: { results: [{ id: 2, name: "Bạc xỉu" }], next: null },
      });

    const records = await inventoryList("products");

    expect(records.map((item) => item.id)).toEqual([1, 2]);
    expect(client.get).toHaveBeenNthCalledWith(1, "/api/v1/products/");
    expect(client.get).toHaveBeenNthCalledWith(2, "/api/v1/products/?page=2");
  });
});
