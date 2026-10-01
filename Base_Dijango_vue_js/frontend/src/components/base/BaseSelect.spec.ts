import { mount } from "@vue/test-utils";
import BaseSelect from "./BaseSelect.vue";

describe("BaseSelect", () => {
  it("supports keyboard navigation without a native select", async () => {
    const wrapper = mount(BaseSelect, {
      props: {
        id: "sort",
        name: "sort",
        modelValue: "popular",
        options: [
          { value: "popular", label: "Phổ biến" },
          { value: "price", label: "Giá tăng dần" },
        ],
      },
    });
    expect(wrapper.find("select").exists()).toBe(false);
    await wrapper.get('[role="combobox"]').trigger("keydown", { key: "ArrowDown" });
    await wrapper.get('[role="listbox"]').trigger("keydown", { key: "ArrowDown" });
    await wrapper.get('[role="listbox"]').trigger("keydown", { key: "Enter" });
    expect(wrapper.emitted("update:modelValue")?.[0]).toEqual(["price"]);
  });
});
