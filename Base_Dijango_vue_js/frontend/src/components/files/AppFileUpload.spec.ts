import { mount } from "@vue/test-utils";

import AppFileUpload from "./AppFileUpload.vue";

describe("AppFileUpload", () => {
  it("rejects files larger than the configured limit", async () => {
    const wrapper = mount(AppFileUpload, { props: { id: "file", maxSizeMb: 1 } });
    const input = wrapper.get('input[type="file"]');
    const file = new File([new Uint8Array(1024 * 1024 + 1)], "large.xlsx");

    Object.defineProperty(input.element, "files", { value: [file], configurable: true });
    await input.trigger("change");

    expect(wrapper.get('[role="alert"]').text()).toContain("1 MB");
    expect(wrapper.emitted("select")?.[0]).toEqual([null]);
  });
});
