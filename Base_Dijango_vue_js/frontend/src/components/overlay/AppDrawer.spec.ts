import { mount } from "@vue/test-utils";
import { nextTick } from "vue";
import AppDrawer from "./AppDrawer.vue";

describe("AppDrawer", () => {
  it("opens on the right, closes with Escape and restores focus", async () => {
    const trigger = document.createElement("button");
    document.body.appendChild(trigger);
    trigger.focus();
    const wrapper = mount(AppDrawer, {
      attachTo: document.body,
      props: { open: false, title: "Giỏ hàng" },
      slots: { default: '<button id="drawer-action">Thao tác</button>' },
    });

    await wrapper.setProps({ open: true });
    await nextTick();
    expect(document.querySelector('[role="dialog"]')).not.toBeNull();
    expect(document.activeElement?.getAttribute("aria-label")).toBe("Đóng ngăn kéo");

    document
      .querySelector('[role="dialog"]')
      ?.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
    expect(wrapper.emitted("close")).toHaveLength(1);

    await wrapper.setProps({ open: false });
    expect(document.activeElement).toBe(trigger);
    wrapper.unmount();
    trigger.remove();
  });
});
