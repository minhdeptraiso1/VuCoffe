import { mount } from "@vue/test-utils";

import { MENU_ITEMS } from "../data/menuData";
import MenuProductCard from "./MenuProductCard.vue";

describe("MenuProductCard", () => {
  it("shows decision information and emits the selected item", async () => {
    const item = MENU_ITEMS[0];
    if (!item) throw new Error("Menu fixture is required");
    const wrapper = mount(MenuProductCard, { props: { item } });

    expect(wrapper.text()).toContain(item.name);
    expect(wrapper.text()).toContain(item.formattedPrice);
    expect(wrapper.get("button").attributes("aria-label")).toContain(item.name);

    await wrapper.get("button").trigger("click");
    expect(wrapper.emitted("select")?.[0]).toEqual([item]);
  });
});
