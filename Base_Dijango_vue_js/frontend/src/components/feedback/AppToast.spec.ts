import { createPinia, setActivePinia } from "pinia";
import { mount } from "@vue/test-utils";

import { useToastStore } from "@/app/stores/toast";
import AppToast from "./AppToast.vue";

describe("AppToast", () => {
  it("appears at the top right and dismisses when the toast is clicked", async () => {
    const pinia = createPinia();
    setActivePinia(pinia);
    const toast = useToastStore();
    const wrapper = mount(AppToast, { global: { plugins: [pinia] } });

    toast.show("Đã lưu thay đổi.", "success");
    await wrapper.vm.$nextTick();

    const notification = wrapper.get('[role="status"]');
    expect(notification.classes()).toContain("top-4");
    expect(notification.text()).not.toContain("Đóng");
    await notification.trigger("click");
    expect(toast.message).toBe("");
  });
});
