<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { ArrowRight, Clock, Coffee, Laptop, MapPin, Phone, Star, Trees } from "lucide-vue-next";

import AppLogo from "@/components/brand/AppLogo.vue";
import DrinkIllustration from "@/components/brand/DrinkIllustration.vue";
import PublicHeader from "@/components/layout/PublicHeader.vue";
import { MENU_ITEMS } from "@/modules/menu/data/menuData";

const root = ref<HTMLElement | null>(null);
let cleanupMotion: (() => void) | undefined;
const getRoot = () => root.value;

const signatureShowcaseItems = MENU_ITEMS.slice(0, 3);

const activeCraftStep = ref<number>(0);
const craftStepImages = [
  {
    src: "/images/craft-step-1-cherries.jpg",
    alt: "Những chùm quả cà phê chín mọng trên cành tại Cầu Đất & Buôn Ma Thuột",
  },
  {
    src: "/images/craft-step-2-roasting.jpg",
    alt: "Hạt cà phê rang mộc mẻ nhỏ bằng khí nóng đối lưu",
  },
  {
    src: "/images/craft-step-3-extraction.jpg",
    alt: "Chiết xuất espresso với lớp crema vàng óng sánh mịn",
  },
  {
    src: "/images/craft-coffee-cup.jpg",
    alt: "Tách cà phê thủ công hoàn hảo với lớp latte art thơm ngát",
  },
];

onMounted(async () => {
  if (globalThis.matchMedia("(prefers-reduced-motion: reduce)").matches || !getRoot()) return;
  const [{ gsap }, { ScrollTrigger }] = await Promise.all([
    import("gsap"),
    import("gsap/ScrollTrigger"),
  ]);
  const rootElement = getRoot();
  if (!rootElement) return;
  gsap.registerPlugin(ScrollTrigger);
  const context = gsap.context(() => {
    gsap.from("[data-reveal]", {
      opacity: 0,
      y: 20,
      duration: 0.6,
      stagger: 0.08,
      ease: "power2.out",
    });
    rootElement.querySelectorAll<HTMLElement>("[data-scroll-reveal]").forEach((section) => {
      gsap.from(section.children, {
        opacity: 0,
        y: 24,
        duration: 1.1,
        stagger: 0.14,
        ease: "power2.out",
        scrollTrigger: { trigger: section, start: "top 80%", once: true },
      });
    });

    gsap.to("[data-hero-visual]", {
      yPercent: 8,
      rotateX: 2,
      rotateY: -4,
      transformOrigin: "50% 50%",
      ease: "none",
      scrollTrigger: {
        trigger: "[data-hero-visual]",
        start: "top top+=72",
        end: "bottom top",
        scrub: 1.4,
      },
    });

    // Crossfade sticky craft images on scroll
    rootElement.querySelectorAll<HTMLElement>("[data-craft-step]").forEach((stepEl, idx) => {
      ScrollTrigger.create({
        trigger: stepEl,
        start: "top 80%",
        end: "bottom 38%",
        onEnter: () => {
          activeCraftStep.value = idx;
        },
        onEnterBack: () => {
          activeCraftStep.value = idx;
        },
      });
    });
  }, rootElement);
  ScrollTrigger.refresh();
  cleanupMotion = () => {
    context.revert();
  };
});

onBeforeUnmount(() => cleanupMotion?.());
</script>

<template>
  <div
    ref="root"
    class="min-h-screen bg-[var(--color-espresso-dark)] text-stone-100 selection:bg-[#dfab71] selection:text-[#160e08]"
  >
    <PublicHeader />

    <main>
      <!-- Hero Section (Dark Espresso & Splashing Coffee Cup Mockup) -->
      <section
        class="relative overflow-hidden bg-[#160e08] pb-16 pt-10 sm:pb-20 sm:pt-14 lg:pb-24 lg:pt-16"
      >
        <!-- Ambient Warm Spotlight -->
        <div
          class="pointer-events-none absolute -top-20 right-1/4 -z-10 h-[500px] w-[500px] rounded-full bg-[#c58940]/15 blur-[120px]"
        ></div>

        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid items-center gap-8 lg:grid-cols-[0.78fr_1.32fr] lg:gap-2">
            <!-- Left Hero Content -->
            <div>
              <!-- Main Hero Headline (Editorial Serif Style) -->
              <h1
                data-reveal
                class="font-[var(--font-display)] text-4xl font-bold leading-[1.08] tracking-tight text-white sm:text-5xl lg:text-6xl"
              >
                Khám phá nghệ thuật<br />
                của một tách cà phê<br />
                <span class="text-[#dfab71] italic font-serif">hoàn hảo</span>
              </h1>

              <!-- Hero Subtitle -->
              <p
                data-reveal
                class="mt-6 max-w-xl text-base leading-relaxed text-stone-300 sm:text-lg font-light"
              >
                Cà phê rang mộc mẻ nhỏ, pha tươi mỗi ngày để giữ trọn vị đậm và hậu ngọt tự nhiên.
              </p>

              <!-- Hero CTAs -->
              <div data-reveal class="mt-8 flex flex-wrap items-center gap-4">
                <RouterLink
                  to="/menu"
                  class="inline-flex items-center gap-2.5 rounded-full bg-white px-7 py-3.5 text-sm font-bold text-[#160e08] shadow-lg shadow-black/40 transition-all duration-300 hover:bg-[#dfab71] hover:scale-103"
                >
                  <span>Đặt món ngay</span>
                  <ArrowRight class="size-4" />
                </RouterLink>

                <a
                  href="#coffee-heaven"
                  class="inline-flex items-center gap-2 rounded-full border border-white/25 bg-white/5 px-6 py-3.5 text-sm font-medium text-stone-200 backdrop-blur-xs transition-all duration-200 hover:bg-white/15 hover:border-white/50 hover:text-white"
                >
                  <span>Khám phá thêm</span>
                </a>
              </div>

              <!-- Hero Stats Counters (Guaranteed on ONE Single Horizontal Line) -->
              <div
                data-reveal
                class="mt-10 flex flex-nowrap items-center gap-4 overflow-x-auto border-t border-white/15 pt-6 sm:gap-8 no-scrollbar"
              >
                <div class="shrink-0">
                  <p
                    class="font-[var(--font-display)] text-2xl sm:text-3xl lg:text-4xl font-bold text-white whitespace-nowrap"
                  >
                    50+
                  </p>
                  <p
                    class="mt-1 text-[0.65rem] sm:text-[0.7rem] font-semibold tracking-wider text-stone-400 uppercase whitespace-nowrap"
                  >
                    Món trong thực đơn
                  </p>
                </div>
                <div class="h-10 w-px bg-white/15 shrink-0"></div>
                <div class="shrink-0">
                  <p
                    class="font-[var(--font-display)] text-2xl sm:text-3xl lg:text-4xl font-bold text-white whitespace-nowrap"
                  >
                    20+
                  </p>
                  <p
                    class="mt-1 text-[0.65rem] sm:text-[0.7rem] font-semibold tracking-wider text-stone-400 uppercase whitespace-nowrap"
                  >
                    Đơn đang phục vụ
                  </p>
                </div>
                <div class="h-10 w-px bg-white/15 shrink-0"></div>
                <div class="shrink-0">
                  <p
                    class="font-[var(--font-display)] text-2xl sm:text-3xl lg:text-4xl font-bold text-[#dfab71] whitespace-nowrap"
                  >
                    2k+
                  </p>
                  <p
                    class="mt-1 text-[0.65rem] sm:text-[0.7rem] font-semibold tracking-wider text-stone-400 uppercase whitespace-nowrap"
                  >
                    Khách hàng hài lòng
                  </p>
                </div>
              </div>
            </div>

            <!-- Right Hero Visual: Centered in Right Column with Feathered Radial Boundary -->
            <div
              data-reveal
              data-hero-visual
              class="relative flex items-center justify-center [perspective:1200px] [transform-style:preserve-3d] will-change-transform lg:-mr-12 xl:-mr-20"
            >
              <div
                class="relative mx-auto flex w-full max-w-2xl items-center justify-center lg:max-w-3xl xl:max-w-[54rem]"
              >
                <!-- Golden Ambient Aura -->
                <div
                  class="absolute inset-0 rounded-full bg-gradient-to-tr from-[#94552e]/50 to-[#dfab71]/35 blur-[100px] pointer-events-none scale-125"
                ></div>

                <!-- Photorealistic Splashing Coffee Cup with Feathered Radial Boundary -->
                <div class="hero-coffee-visual relative z-10 w-full overflow-hidden">
                  <img
                    src="/images/hero-coffee-splash.jpg"
                    alt="Tách cà phê Kim Thành với dòng cà phê và hạt cà phê rang bắn tung sống động"
                    class="h-auto w-full scale-110 object-contain transition-transform duration-700 hover:scale-[1.14] sm:scale-[1.12] lg:scale-[1.16] lg:hover:scale-[1.2]"
                    loading="eager"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 2: "Coffee Heaven" (Matching bottom half of mockup) -->
      <section
        id="coffee-heaven"
        class="relative overflow-hidden bg-[var(--color-cream-bg)] py-16 text-[#1c130d] sm:py-20"
      >
        <!-- Delicate Watermark / Texture in Background -->
        <div
          aria-hidden="true"
          class="pointer-events-none absolute -left-10 bottom-0 select-none font-[var(--font-display)] text-[12vw] font-black text-[#1c130d]/[0.03]"
        >
          Kim Thành
        </div>

        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid items-center gap-12 lg:grid-cols-2 lg:gap-16">
            <!-- Left Column: Realistic Barista Latte Art Photo with Thin Geometric Accents -->
            <div data-scroll-reveal class="relative flex justify-center">
              <div class="relative w-full max-w-md">
                <div class="relative overflow-hidden rounded-3xl shadow-xl">
                  <img
                    src="/images/barista-latte-art.jpg"
                    alt="Barista Kim Thành Coffee đang tỉ mỉ rót nghệ thuật latte art trên tách cà phê nóng"
                    class="h-80 w-full object-cover transition-transform duration-700 hover:scale-105 sm:h-96"
                    loading="lazy"
                  />
                </div>
              </div>
            </div>

            <!-- Right Column: Coffee Heaven Story & CTA -->
            <div data-scroll-reveal>
              <div
                class="inline-flex items-center gap-2 text-xs font-bold tracking-widest text-[#b85c38] uppercase"
              >
                <span>Về Kim Thành</span>
              </div>

              <!-- High Contrast Serif Title -->
              <h2
                class="mt-3 font-[var(--font-display)] text-4xl sm:text-5xl font-bold tracking-tight text-[#1c130d] leading-[1.15]"
              >
                Một quán cà phê làm bằng sự tử tế
              </h2>

              <p class="mt-5 text-base leading-relaxed text-[#6f6256] sm:text-lg">
                Kim Thành theo đuổi cà phê rang mộc nguyên bản từ hạt Tây Nguyên và Cầu Đất. Chúng
                tôi rang mẻ nhỏ, không tẩm hương liệu và pha từng ly khi khách gọi — để mỗi lần ghé
                quán đều gần gũi, chỉn chu và đúng vị Việt.
              </p>

              <!-- Pill Black Button matching mockup -->
              <div class="mt-8 flex items-center gap-4">
                <RouterLink
                  to="/menu"
                  class="inline-flex items-center gap-2.5 rounded-full bg-[#1c130d] px-8 py-3.5 text-sm font-semibold text-white shadow-md transition-all duration-300 hover:bg-[#3d2417] hover:scale-103"
                >
                  <span>Xem thực đơn</span>
                  <ArrowRight class="size-4" />
                </RouterLink>
                <a
                  href="#ambiance"
                  class="text-xs font-semibold text-[#6f6256] hover:text-[#1c130d] transition-colors underline underline-offset-4"
                >
                  Khám phá không gian quán
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 3: Signature Menu Showcase with Real Beverage Photography -->
      <section
        id="menu"
        class="border-t border-[#e2d4c0] bg-[var(--color-cream-surface)] py-16 text-[#1c130d] sm:py-20"
      >
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <!-- Section Header -->
          <div class="text-center max-w-2xl mx-auto">
            <h2
              class="font-[var(--font-display)] text-3xl font-bold tracking-tight text-[#1c130d] sm:text-4xl"
            >
              Món được yêu thích tại Kim Thành
            </h2>
            <p class="mt-3 text-[#6f6256]">Ba lựa chọn nổi bật để bạn bắt đầu nhanh.</p>
          </div>

          <!-- Product Grid with Real Photography -->
          <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div
              v-for="item in signatureShowcaseItems"
              :key="item.id"
              class="group relative flex flex-col justify-between rounded-2xl border border-[#e2d4c0] bg-white p-5 shadow-xs transition-all duration-300 hover:shadow-xl hover:border-[#6f3f25] hover:-translate-y-1"
            >
              <div>
                <!-- Real Photography Component -->
                <DrinkIllustration
                  :type="item.illustrationType"
                  :image="item.image"
                  :alt="item.name"
                  size="sm"
                  class="mb-4"
                />

                <div class="flex items-center justify-between gap-2">
                  <span
                    class="rounded-md px-2.5 py-0.5 text-[0.65rem] font-bold tracking-wide uppercase"
                    :class="
                      item.isBestSeller ? 'bg-[#b85c38] text-white' : 'bg-[#ead8c6] text-[#6f3f25]'
                    "
                  >
                    {{ item.tag }}
                  </span>
                  <span class="font-bold text-lg text-[#6f3f25] font-[var(--font-display)]">
                    {{ item.formattedPrice }}
                  </span>
                </div>

                <h3
                  class="mt-3 font-[var(--font-display)] text-xl font-bold text-[#1c130d] group-hover:text-[#6f3f25] transition-colors"
                >
                  {{ item.name }}
                </h3>

                <p class="mt-2 text-xs leading-relaxed text-[#6f6256] line-clamp-2 font-light">
                  {{ item.description }}
                </p>
              </div>

              <div
                class="mt-5 pt-3.5 border-t border-[#e2d4c0]/70 flex items-center justify-between"
              >
                <div class="flex items-center gap-1 text-[0.7rem] text-[#6f6256]">
                  <Star class="size-3.5 fill-[#c58940] text-[#c58940]" />
                  <span class="font-bold text-[#1c130d]">{{ item.rating }}</span>
                  <span>({{ item.reviewCount }})</span>
                </div>
                <RouterLink
                  to="/menu"
                  class="text-xs font-bold text-[#6f3f25] hover:text-[#b85c38] transition-colors inline-flex items-center gap-1"
                >
                  <span>Tùy chỉnh & Đặt món</span>
                  <ArrowRight class="size-3" />
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 4: Craft Journey & Artisanal Coffee Showcase -->
      <section
        id="process"
        class="border-t border-[#e2d4c0] bg-[var(--color-cream-bg)] py-16 sm:py-24 text-[#1c130d]"
      >
        <div
          class="mx-auto grid max-w-7xl gap-10 px-4 sm:px-6 lg:grid-cols-[1.1fr_1fr] lg:gap-14 xl:gap-20 lg:px-8 items-start"
        >
          <!-- Craft Coffee Showcase Card (Sticky Pure Image, Centered Vertically on Screen, Enlarged) -->
          <div
            class="lg:sticky lg:top-20 lg:h-[calc(100vh-5rem)] flex items-center justify-center py-4"
          >
            <div
              class="w-full max-w-lg lg:max-w-xl rounded-[2.5rem] border border-[#d8c8b5] bg-white p-4 sm:p-5 shadow-2xl overflow-hidden transition-all duration-300"
            >
              <div
                class="relative overflow-hidden rounded-[2rem] aspect-square bg-[#1c130d] w-full shadow-inner"
              >
                <img
                  v-for="(img, idx) in craftStepImages"
                  :key="img.src"
                  :src="img.src"
                  :alt="img.alt"
                  class="absolute inset-0 size-full object-cover transition-all duration-[1200ms] ease-in-out"
                  :class="
                    activeCraftStep === idx
                      ? 'opacity-100 scale-100 z-10'
                      : 'opacity-0 scale-105 z-0'
                  "
                  loading="lazy"
                />
              </div>
            </div>
          </div>

          <!-- Craft Journey Steps -->
          <div class="divide-y divide-[#e2d4c0]">
            <article
              data-craft-step
              data-scroll-reveal
              class="flex min-h-[50vh] flex-col justify-center py-10"
            >
              <p class="text-xs font-bold uppercase tracking-[0.2em] text-[#b85c38]">
                01 · Nguồn Hạt
              </p>
              <h2
                class="mt-3 font-[var(--font-display)] text-3xl font-bold sm:text-4xl text-[#1c130d]"
              >
                Tuyển chọn từ những cao nguyên danh tiếng
              </h2>
              <p class="mt-4 text-base leading-relaxed text-[#6f6256]">
                Hạt chín mọng được tuyển từ Buôn Ma Thuột và Cầu Đất để bảo đảm vị sạch, đồng đều.
              </p>
            </article>

            <article
              data-craft-step
              data-scroll-reveal
              class="flex min-h-[50vh] flex-col justify-center py-10"
            >
              <p class="text-xs font-bold uppercase tracking-[0.2em] text-[#b85c38]">
                02 · Rang Mộc
              </p>
              <h2
                class="mt-3 font-[var(--font-display)] text-3xl font-bold sm:text-4xl text-[#1c130d]"
              >
                Kỹ thuật rang thủ công mẻ nhỏ
              </h2>
              <p class="mt-4 text-base leading-relaxed text-[#6f6256]">
                Rang mộc mẻ nhỏ, không bơ hay hương liệu, giữ lại hương caramel và chocolate tự
                nhiên.
              </p>
            </article>

            <article
              data-craft-step
              data-scroll-reveal
              class="flex min-h-[50vh] flex-col justify-center py-10"
            >
              <p class="text-xs font-bold uppercase tracking-[0.2em] text-[#b85c38]">
                03 · Chiết Xuất
              </p>
              <h2
                class="mt-3 font-[var(--font-display)] text-3xl font-bold sm:text-4xl text-[#1c130d]"
              >
                Tỷ lệ vàng giữa truyền thống & hiện đại
              </h2>
              <p class="mt-4 text-base leading-relaxed text-[#6f6256]">
                Phin Việt và espresso 9 bar được cân chỉnh riêng để mỗi món có độ đậm và hậu vị cân
                bằng.
              </p>
            </article>

            <article
              data-craft-step
              data-scroll-reveal
              class="flex min-h-[50vh] flex-col justify-center py-10"
            >
              <p class="text-xs font-bold uppercase tracking-[0.2em] text-[#b85c38]">
                04 · Thưởng Thức
              </p>
              <h2
                class="mt-3 font-[var(--font-display)] text-3xl font-bold sm:text-4xl text-[#1c130d]"
              >
                Đậm đà từng khoảnh khắc gặp gỡ
              </h2>
              <p class="mt-4 text-base leading-relaxed text-[#6f6256]">
                Một ly cà phê ngon để bắt đầu ngày mới, làm việc hoặc gặp gỡ những người thân quen.
              </p>
            </article>
            <div aria-hidden="true" class="hidden h-[24vh] lg:block"></div>
          </div>
        </div>
      </section>

      <!-- Section 5: Ambiance & Space with Real Cafe Photography -->
      <section
        id="ambiance"
        class="border-t border-[#e2d4c0] bg-white py-16 text-[#1c130d] sm:py-20"
      >
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="text-center max-w-2xl mx-auto">
            <h2
              class="font-[var(--font-display)] text-3xl font-bold tracking-tight text-[#1c130d] sm:text-4xl"
            >
              Nơi Dừng Chân Ấm Áp Giữa Lòng Đô Thị
            </h2>
            <p class="mt-3 text-[#6f6256] text-base font-light">
              Ba góc ngồi cho làm việc, trò chuyện và thư giãn.
            </p>
          </div>

          <div class="mt-14 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <!-- Space 1: Workspace & Reading -->
            <div
              data-scroll-reveal
              class="group overflow-hidden rounded-3xl border border-[#e2d4c0] bg-[var(--color-cream-surface)] shadow-xs transition-all duration-300 hover:shadow-xl hover:border-[#6f3f25] hover:-translate-y-1 flex flex-col justify-between"
            >
              <div>
                <div class="relative h-60 w-full overflow-hidden bg-stone-100">
                  <img
                    src="/images/ambiance-workspace.jpg"
                    alt="Không gian bàn dài làm việc và đọc sách tại Kim Thành Coffee"
                    class="size-full object-cover transition-transform duration-700 group-hover:scale-105"
                    loading="lazy"
                  />
                  <span
                    class="absolute left-4 top-4 rounded-full bg-[#160e08]/75 backdrop-blur-xs px-3 py-1 text-xs font-semibold text-white"
                  >
                    Wifi 200Mbps · Ổ cắm riêng
                  </span>
                </div>
                <div class="p-6">
                  <div
                    class="flex items-center gap-2 text-xs font-bold text-[#b85c38] uppercase tracking-wider"
                  >
                    <Laptop class="size-4" />
                    <span>Khu Làm Việc & Đọc Sách</span>
                  </div>
                  <h3
                    class="mt-2 font-[var(--font-display)] text-xl font-bold text-[#1c130d] group-hover:text-[#6f3f25] transition-colors"
                  >
                    Góc làm việc & Học tập
                  </h3>
                  <p class="mt-2 text-sm leading-relaxed text-[#6f6256] font-light">
                    Bàn rộng, ổ cắm riêng và Wifi ổn định cho một buổi làm việc tập trung.
                  </p>
                </div>
              </div>
            </div>

            <!-- Space 2: Outdoor Garden Patio -->
            <div
              data-scroll-reveal
              class="group overflow-hidden rounded-3xl border border-[#e2d4c0] bg-[var(--color-cream-surface)] shadow-xs transition-all duration-300 hover:shadow-xl hover:border-[#6f3f25] hover:-translate-y-1 flex flex-col justify-between"
            >
              <div>
                <div class="relative h-60 w-full overflow-hidden bg-stone-100">
                  <img
                    src="/images/ambiance-patio.jpg"
                    alt="Góc sân hiên ngoài trời rợp bóng cây xanh tại quán"
                    class="size-full object-cover transition-transform duration-700 group-hover:scale-105"
                    loading="lazy"
                  />
                  <span
                    class="absolute left-4 top-4 rounded-full bg-[#160e08]/75 backdrop-blur-xs px-3 py-1 text-xs font-semibold text-white"
                  >
                    Không gian mở thoáng đãng
                  </span>
                </div>
                <div class="p-6">
                  <div
                    class="flex items-center gap-2 text-xs font-bold text-[#b85c38] uppercase tracking-wider"
                  >
                    <Trees class="size-4" />
                    <span>Sân Vườn Nhiệt Đới</span>
                  </div>
                  <h3
                    class="mt-2 font-[var(--font-display)] text-xl font-bold text-[#1c130d] group-hover:text-[#6f3f25] transition-colors"
                  >
                    Góc sân hiên thoáng đãng
                  </h3>
                  <p class="mt-2 text-sm leading-relaxed text-[#6f6256] font-light">
                    Sân hiên nhiều cây xanh, thoáng gió cho những cuộc hẹn thư thả.
                  </p>
                </div>
              </div>
            </div>

            <!-- Space 3: Open Espresso Bar Counter -->
            <div
              data-scroll-reveal
              class="group overflow-hidden rounded-3xl border border-[#e2d4c0] bg-[var(--color-cream-surface)] shadow-xs transition-all duration-300 hover:shadow-xl hover:border-[#6f3f25] hover:-translate-y-1 sm:col-span-2 lg:col-span-1 flex flex-col justify-between"
            >
              <div>
                <div class="relative h-60 w-full overflow-hidden bg-stone-100">
                  <img
                    src="/images/ambiance-counter.jpg"
                    alt="Quầy bar pha chế mở và máy pha cà phê chuyên nghiệp"
                    class="size-full object-cover transition-transform duration-700 group-hover:scale-105"
                    loading="lazy"
                  />
                  <span
                    class="absolute left-4 top-4 rounded-full bg-[#160e08]/75 backdrop-blur-xs px-3 py-1 text-xs font-semibold text-white"
                  >
                    Pha chế trực tiếp tại quầy
                  </span>
                </div>
                <div class="p-6">
                  <div
                    class="flex items-center gap-2 text-xs font-bold text-[#b85c38] uppercase tracking-wider"
                  >
                    <Coffee class="size-4" />
                    <span>Quầy barista thủ công</span>
                  </div>
                  <h3
                    class="mt-2 font-[var(--font-display)] text-xl font-bold text-[#1c130d] group-hover:text-[#6f3f25] transition-colors"
                  >
                    Quầy pha chế mở
                  </h3>
                  <p class="mt-2 text-sm leading-relaxed text-[#6f6256] font-light">
                    Quan sát barista pha từng ly và trò chuyện ngay tại quầy mở.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Store Hours & Contact Banner with Lucide Icons -->
      <section class="border-t border-[#e2d4c0] bg-[var(--color-cream-bg)] py-12 text-[#1c130d]">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid gap-6 sm:grid-cols-3 text-center sm:text-left">
            <div class="flex items-center gap-4 justify-center sm:justify-start">
              <div
                class="size-11 rounded-full bg-[#ead8c6] text-[#6f3f25] flex items-center justify-center shrink-0"
              >
                <MapPin class="size-5" />
              </div>
              <div>
                <p class="text-xs font-semibold text-[#6f6256] uppercase tracking-wider">Địa chỉ</p>
                <p class="font-bold text-[#1c130d]">Kim Thành Coffee House</p>
              </div>
            </div>

            <div class="flex items-center gap-4 justify-center sm:justify-start">
              <div
                class="size-11 rounded-full bg-[#ead8c6] text-[#6f3f25] flex items-center justify-center shrink-0"
              >
                <Clock class="size-5" />
              </div>
              <div>
                <p class="text-xs font-semibold text-[#6f6256] uppercase tracking-wider">
                  Giờ mở cửa
                </p>
                <p class="font-bold text-[#1c130d]">07:00 – 22:30 hàng ngày</p>
              </div>
            </div>

            <div class="flex items-center gap-4 justify-center sm:justify-start">
              <div
                class="size-11 rounded-full bg-[#ead8c6] text-[#6f3f25] flex items-center justify-center shrink-0"
              >
                <Phone class="size-5" />
              </div>
              <div>
                <p class="text-xs font-semibold text-[#6f6256] uppercase tracking-wider">
                  Hotline hỗ trợ
                </p>
                <p class="font-bold text-[#1c130d]">1900 · KIM THÀNH</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer (Deep Espresso Finish) -->
    <footer class="border-t border-white/10 bg-[#140c07] py-14 text-stone-300">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <!-- Col 1: Logo & Mission -->
          <div class="space-y-4">
            <AppLogo variant="pill" size="md" />
            <p class="text-xs leading-relaxed text-stone-400 font-light mt-3">
              Không gian cà phê tử tế, mộc mạc và thân quen. Nơi mỗi tách cà phê đều mang trọn vẹn
              tâm huyết của người pha chế.
            </p>
          </div>

          <!-- Col 2: Navigation -->
          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-white">Khám phá</h4>
            <ul class="mt-3 space-y-2 text-sm text-stone-400">
              <li>
                <RouterLink to="/menu" class="hover:text-[#dfab71] transition-colors">
                  Thực đơn 15+ món
                </RouterLink>
              </li>
              <li>
                <a href="#process" class="hover:text-[#dfab71] transition-colors">
                  Quy trình rang mộc
                </a>
              </li>
              <li>
                <a href="#coffee-heaven" class="hover:text-[#dfab71] transition-colors">
                  Hành trình hạt cà phê
                </a>
              </li>
              <li>
                <a href="#ambiance" class="hover:text-[#dfab71] transition-colors">
                  Không gian quán
                </a>
              </li>
            </ul>
          </div>

          <!-- Col 3: Customer Services -->
          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-white">
              Tài khoản & Dịch vụ
            </h4>
            <ul class="mt-3 space-y-2 text-sm text-stone-400">
              <li>
                <RouterLink to="/login" class="hover:text-[#dfab71] transition-colors">
                  Đăng nhập thành viên
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/register" class="hover:text-[#dfab71] transition-colors">
                  Đăng ký tài khoản
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/account" class="hover:text-[#dfab71] transition-colors">
                  Quản lý đơn hàng
                </RouterLink>
              </li>
            </ul>
          </div>

          <!-- Col 4: Values -->
          <div>
            <h4 class="text-xs font-bold uppercase tracking-wider text-white">Triết lý hạt mộc</h4>
            <p class="mt-3 text-xs leading-relaxed text-stone-400 font-light">
              “Cà phê ngon bắt nguồn từ sự chân thật.” Kim Thành cam kết mang đến những giọt cà phê
              nguyên chất, an lành cho sức khỏe mỗi ngày.
            </p>
          </div>
        </div>

        <div class="mt-12 border-t border-white/10 pt-6 text-center text-xs text-stone-400">
          © 2026 Kim Thành Coffee · Đậm vị truyền thống, trọn vẹn từng khoảnh khắc.
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.hero-coffee-visual {
  -webkit-mask-image: radial-gradient(
    ellipse 50% 50% at 50% 50%,
    #000 40%,
    rgb(0 0 0 / 94%) 58%,
    transparent 100%
  );
  mask-image: radial-gradient(
    ellipse 50% 50% at 50% 50%,
    #000 40%,
    rgb(0 0 0 / 94%) 58%,
    transparent 100%
  );
}

.hero-coffee-visual::after {
  position: absolute;
  inset: 0;
  pointer-events: none;
  content: "";
  background: radial-gradient(
    ellipse 50% 50% at 50% 50%,
    transparent 40%,
    rgb(22 14 8 / 12%) 58%,
    rgb(22 14 8 / 72%) 82%,
    #160e08 100%
  );
}
</style>
