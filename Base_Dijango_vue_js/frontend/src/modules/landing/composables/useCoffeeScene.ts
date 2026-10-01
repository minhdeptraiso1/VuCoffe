import { onBeforeUnmount, onMounted, type Ref, ref } from "vue";

export type SceneStatus = "poster" | "loading" | "ready" | "error";

export function useCoffeeScene(canvas: Ref<HTMLCanvasElement | null>) {
  const status = ref<SceneStatus>("poster");
  let cleanup: (() => void) | undefined;
  let active = true;
  const isActive = () => active;

  onMounted(async () => {
    if (globalThis.matchMedia("(prefers-reduced-motion: reduce)").matches || !canvas.value) return;
    status.value = "loading";
    try {
      const { createCoffeeScene } = await import("./coffeeSceneRuntime");
      if (!isActive()) return;
      const scene = createCoffeeScene(canvas.value);
      let scrollFrame = 0;
      const updateFromScroll = () => {
        const root = globalThis.document.documentElement;
        const maxScroll = Math.max(root.scrollHeight - globalThis.innerHeight, 1);
        scene.setScrollProgress(globalThis.scrollY / maxScroll);
        scrollFrame = 0;
      };
      const onScroll = () => {
        if (scrollFrame) return;
        scrollFrame = globalThis.requestAnimationFrame(updateFromScroll);
      };
      globalThis.addEventListener("scroll", onScroll, { passive: true });
      updateFromScroll();
      cleanup = () => {
        globalThis.cancelAnimationFrame(scrollFrame);
        globalThis.removeEventListener("scroll", onScroll);
        scene.destroy();
      };
      status.value = "ready";
    } catch {
      status.value = "error";
    }
  });

  onBeforeUnmount(() => {
    active = false;
    cleanup?.();
  });
  return { status };
}
