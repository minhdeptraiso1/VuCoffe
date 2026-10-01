import { mount } from "@vue/test-utils";
import { describe, expect, it } from "vitest";

import AppLogo from "./AppLogo.vue";

describe("AppLogo", () => {
  it("renders full logo with brand name and coffee text by default", () => {
    const wrapper = mount(AppLogo);
    expect(wrapper.text()).toContain("KIM THÀNH");
    expect(wrapper.text()).toContain("COFFEE");
    expect(wrapper.find("svg").exists()).toBe(true);
  });

  it("renders only mark icon when variant is mark", () => {
    const wrapper = mount(AppLogo, { props: { variant: "mark" } });
    expect(wrapper.find("svg").exists()).toBe(true);
    expect(wrapper.text()).toBe("");
  });

  it("renders compact single-line title when variant is compact", () => {
    const wrapper = mount(AppLogo, { props: { variant: "compact" } });
    expect(wrapper.text()).toContain("Kim Thành");
    expect(wrapper.text()).toContain("Coffee");
  });

  it("renders tagline when showTagline is enabled", () => {
    const wrapper = mount(AppLogo, { props: { showTagline: true } });
    expect(wrapper.text()).toContain("Rang mộc · Đậm vị truyền thống");
  });
});
