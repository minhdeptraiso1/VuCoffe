import { mount } from "@vue/test-utils";
import { nextTick } from "vue";

import AppModal from "./AppModal.vue";

describe("AppModal", () => {
  it("focuses the first control, closes on Escape and restores focus", async () => {
    const trigger = document.createElement("button");
    document.body.appendChild(trigger);
    trigger.focus();

    const wrapper = mount(AppModal, {
      attachTo: document.body,
      props: { open: false, title: "Xác nhận" },
      slots: { default: '<button id="inside">Thao tác</button>' },
    });

    await wrapper.setProps({ open: true });
    await nextTick();
    expect(document.activeElement?.getAttribute("aria-label")).toBe("Đóng hộp thoại");

    const dialog = document.querySelector('[role="dialog"]');
    dialog?.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
    await nextTick();
    expect(wrapper.emitted("close")).toHaveLength(1);

    await wrapper.setProps({ open: false });
    expect(document.activeElement).toBe(trigger);
    wrapper.unmount();
    trigger.remove();
  });
});
