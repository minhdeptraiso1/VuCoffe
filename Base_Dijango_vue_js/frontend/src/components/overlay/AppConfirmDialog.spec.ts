import { mount } from "@vue/test-utils";
import { nextTick } from "vue";

import AppConfirmDialog from "./AppConfirmDialog.vue";

describe("AppConfirmDialog", () => {
  it("submits a semantic confirmation form", async () => {
    const wrapper = mount(AppConfirmDialog, {
      attachTo: document.body,
      props: { open: true, title: "Xác nhận" },
    });
    await nextTick();

    const form = document.querySelector<HTMLFormElement>('form[id^="confirm-"]');
    form?.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
    await nextTick();

    expect(wrapper.emitted("confirm")).toHaveLength(1);
    wrapper.unmount();
  });
});
