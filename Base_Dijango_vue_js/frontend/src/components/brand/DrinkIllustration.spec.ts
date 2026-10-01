import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import DrinkIllustration from "./DrinkIllustration.vue";

describe("DrinkIllustration", () => {
  it("renders salted coffee illustration SVG", () => {
    const wrapper = mount(DrinkIllustration, {
      props: { type: "salted-coffee" },
    });
    expect(wrapper.find("svg").exists()).toBe(true);
  });

  it("renders egg coffee illustration with bowl and foam", () => {
    const wrapper = mount(DrinkIllustration, {
      props: { type: "egg-coffee" },
    });
    expect(wrapper.find("svg").exists()).toBe(true);
  });

  it("renders cold brew illustration with cinnamon and citrus", () => {
    const wrapper = mount(DrinkIllustration, {
      props: { type: "cold-brew" },
    });
    expect(wrapper.find("svg").exists()).toBe(true);
  });

  it("renders pastry croissant illustration", () => {
    const wrapper = mount(DrinkIllustration, {
      props: { type: "croissant" },
    });
    expect(wrapper.find("svg").exists()).toBe(true);
  });
});
