<script setup lang="ts">
import { computed } from "vue";
import type { MenuItem } from "@/modules/menu/data/menuData";

interface Props {
  type: MenuItem["illustrationType"];
  size?: "xs" | "sm" | "md" | "lg";
  image?: string;
  alt?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: "md",
  image: "",
  alt: "",
});

const defaultPhotoMap: Record<string, string> = {
  "salted-coffee":
    "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=800&q=80",
  "egg-coffee":
    "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=800&q=80",
  "bac-xiu":
    "https://images.unsplash.com/photo-1572442388796-11668ba67e53?auto=format&fit=crop&w=800&q=80",
  "milk-coffee":
    "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=800&q=80",
  "black-coffee":
    "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80",
  latte:
    "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=800&q=80",
  cappuccino:
    "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=800&q=80",
  "cold-brew":
    "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=800&q=80",
  "peach-tea":
    "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=800&q=80",
  "fruit-tea":
    "https://images.unsplash.com/photo-1497534446932-c925b458314e?auto=format&fit=crop&w=800&q=80",
  matcha:
    "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=800&q=80",
  croissant:
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=800&q=80",
  tiramisu:
    "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=800&q=80",
  cheesecake:
    "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=800&q=80",
};

const resolvedImage = computed(() => {
  return props.image || defaultPhotoMap[props.type] || "";
});
</script>

<template>
  <div
    class="relative flex items-center justify-center overflow-hidden rounded-2xl transition-transform duration-300 group-hover:scale-101 select-none shadow-sm bg-[var(--color-surface-subtle)]"
    :class="{
      'h-20 w-20': size === 'xs',
      'h-44 w-full': size === 'sm',
      'h-56 w-full': size === 'md',
      'h-72 w-full': size === 'lg',
    }"
  >
    <!-- Real Photography of beverage / pastry -->
    <img
      v-if="resolvedImage"
      :src="resolvedImage"
      :alt="alt || type || 'Thức uống Kim Thành'"
      class="absolute inset-0 h-full w-full object-cover transition-transform duration-500 ease-out group-hover:scale-105"
      loading="lazy"
    />

    <!-- Subtle vignette overlay on image for luxury editorial contrast -->
    <div
      v-if="resolvedImage"
      class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-black/10 opacity-70 transition-opacity duration-300 group-hover:opacity-40"
    ></div>

    <!-- Fallback / Accessible SVG Illustrations -->
    <svg
      v-show="!resolvedImage"
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      class="relative z-10 h-full max-h-[90%] w-auto drop-shadow-md transition-transform duration-300 group-hover:-translate-y-1"
    >
      <!-- ============================================== -->
      <!-- 1. CÀ PHÊ MUỐI KIM THÀNH (Salted Coffee) -->
      <!-- ============================================== -->
      <g v-if="type === 'salted-coffee'">
        <!-- Glass body -->
        <path
          d="M68 55 L75 160 C75 166, 82 170, 100 170 C118 170, 125 166, 125 160 L132 55 Z"
          fill="rgba(255,255,255,0.25)"
          stroke="#C8B29B"
          stroke-width="2"
        />
        <!-- Bottom espresso layer -->
        <path
          d="M74 135 L75 160 C75 165, 82 168, 100 168 C118 168, 125 165, 125 160 L126 135 Z"
          fill="#2E170C"
        />
        <!-- Coffee & milk blend middle layer -->
        <path d="M72 92 L74 135 L126 135 L128 92 Z" fill="#753F20" />
        <!-- Swirl streaks -->
        <path
          d="M78 105 Q100 120 122 110"
          stroke="#C59670"
          stroke-width="4"
          stroke-linecap="round"
          opacity="0.6"
        />
        <path
          d="M80 122 Q100 135 118 126"
          stroke="#DDBE9B"
          stroke-width="3"
          stroke-linecap="round"
          opacity="0.5"
        />
        <!-- Salted Cream Foam Cap (Thick white sea salt foam) -->
        <path
          d="M68 55 C68 55, 78 50, 100 50 C122 50, 132 55, 132 55 L130 92 C120 96, 105 91, 100 93 C95 95, 80 96, 70 92 Z"
          fill="#FFFDF8"
        />
        <!-- Foam bubbles / Salt flakes -->
        <ellipse cx="100" cy="53" rx="31" ry="5" fill="#FAF6EE" stroke="#E5DACD" stroke-width="1" />
        <circle cx="94" cy="53" r="1.5" fill="#C58940" />
        <circle cx="106" cy="52" r="1.5" fill="#C58940" />
        <circle cx="100" cy="55" r="1.2" fill="#8F5434" />
        <!-- Sea salt crystal sparkles -->
        <polygon
          points="100,42 102,46 106,47 103,50 104,54 100,51 96,54 97,50 94,47 98,46"
          fill="#C58940"
          opacity="0.8"
        />
        <!-- Ice cubes in glass -->
        <rect
          x="85"
          y="98"
          width="16"
          height="16"
          rx="3"
          transform="rotate(15 85 98)"
          fill="rgba(255,255,255,0.4)"
          stroke="rgba(255,255,255,0.7)"
          stroke-width="1.2"
        />
        <!-- Glass reflection shine -->
        <path
          d="M72 65 L76 155"
          stroke="rgba(255,255,255,0.6)"
          stroke-width="2.5"
          stroke-linecap="round"
        />
      </g>

      <!-- ============================================== -->
      <!-- 2. CÀ PHÊ TRỨNG HANOIAN (Egg Coffee) -->
      <!-- ============================================== -->
      <g v-else-if="type === 'egg-coffee'">
        <!-- Hot water glass bowl cradle -->
        <ellipse
          cx="100"
          cy="165"
          rx="48"
          ry="12"
          fill="#EAD9C6"
          stroke="#D8C5B0"
          stroke-width="2"
        />
        <!-- Ceramic cup body inside bowl -->
        <path
          d="M64 85 C64 140, 80 155, 100 155 C120 155, 136 140, 136 85 Z"
          fill="#FCFAF6"
          stroke="#C8B39B"
          stroke-width="2"
        />
        <!-- Cup handle -->
        <path
          d="M134 95 C146 95, 150 110, 150 120 C150 130, 142 135, 132 135"
          stroke="#FCFAF6"
          stroke-width="6"
          stroke-linecap="round"
          fill="none"
        />
        <path
          d="M134 95 C146 95, 150 110, 150 120 C150 130, 142 135, 132 135"
          stroke="#C8B39B"
          stroke-width="2"
          stroke-linecap="round"
          fill="none"
        />
        <!-- Dark espresso coffee lower layer -->
        <path d="M70 125 C75 142, 85 152, 100 152 C115 152, 125 142, 130 125 Z" fill="#36170A" />
        <!-- Golden Velvety Egg Foam Cap -->
        <path
          d="M65 85 C65 72, 80 66, 100 66 C120 66, 135 72, 135 85 C135 110, 125 126, 100 126 C75 126, 65 110, 65 85 Z"
          fill="#F4C653"
        />
        <ellipse cx="100" cy="74" rx="34" ry="9" fill="#F8D373" />
        <!-- Cacao powder sprinkles on top of egg foam -->
        <circle cx="92" cy="73" r="1.5" fill="#422013" />
        <circle cx="104" cy="72" r="2" fill="#422013" />
        <circle cx="98" cy="76" r="1.2" fill="#422013" />
        <circle cx="110" cy="75" r="1.4" fill="#422013" />
        <circle cx="88" cy="76" r="1.2" fill="#422013" />
        <!-- Gold rim line on cup -->
        <path d="M64 85 C75 89, 125 89, 136 85" stroke="#C58940" stroke-width="1.8" fill="none" />
        <!-- Rising steam curls -->
        <path
          d="M94 58 Q90 48 95 40"
          stroke="#C58940"
          stroke-width="2"
          stroke-linecap="round"
          opacity="0.7"
          fill="none"
        />
        <path
          d="M104 56 Q108 45 103 36"
          stroke="#C58940"
          stroke-width="2"
          stroke-linecap="round"
          opacity="0.7"
          fill="none"
        />
      </g>

      <!-- ============================================== -->
      <!-- 3. BẠC XỈU CỐT DỪA 3 TẦNG (Bac Xiu Coconut) -->
      <!-- ============================================== -->
      <g v-else-if="type === 'bac-xiu'">
        <!-- Tall fluted glass -->
        <path
          d="M72 45 L78 165 C78 170, 85 174, 100 174 C115 174, 122 170, 122 165 L128 45 Z"
          fill="rgba(255,255,255,0.3)"
          stroke="#D4C0A8"
          stroke-width="2"
        />
        <!-- Tier 1 (Bottom): Condensed milk -->
        <path
          d="M77 142 L78 165 C78 169, 85 172, 100 172 C115 172, 122 169, 122 165 L123 142 Z"
          fill="#FDF3CE"
        />
        <!-- Tier 2 (Middle): Fresh Coconut Milk layer -->
        <path d="M75 92 L77 142 L123 142 L125 92 Z" fill="#FFFCF5" />
        <!-- Tier 3 (Top): Dark coffee crema layer -->
        <path d="M72 45 L75 92 L125 92 L128 45 Z" fill="#542B14" />
        <!-- Crema crown -->
        <ellipse cx="100" cy="46" rx="27" ry="5" fill="#9E5D30" />
        <!-- Straw with stripes -->
        <path d="M112 25 L106 150" stroke="#C58940" stroke-width="5" stroke-linecap="round" />
        <path
          d="M112 25 L106 150"
          stroke="#FFFDF7"
          stroke-width="2"
          stroke-dasharray="8 8"
          stroke-linecap="round"
        />
        <!-- Coconut flakes garnish on rim -->
        <rect
          x="82"
          y="44"
          width="7"
          height="2.5"
          rx="1"
          transform="rotate(-10 82 44)"
          fill="#FFFDF7"
        />
        <rect
          x="114"
          y="45"
          width="8"
          height="2.5"
          rx="1"
          transform="rotate(15 114 45)"
          fill="#FFFDF7"
        />
        <!-- Ice cubes -->
        <rect
          x="88"
          y="75"
          width="18"
          height="18"
          rx="3"
          transform="rotate(8 88 75)"
          fill="rgba(255,255,255,0.45)"
          stroke="rgba(255,255,255,0.7)"
          stroke-width="1.2"
        />
      </g>

      <!-- ============================================== -->
      <!-- 4. COLD BREW CAM QUẾ (Cold Brew Citrus) -->
      <!-- ============================================== -->
      <g v-else-if="type === 'cold-brew'">
        <!-- Tumbler glass -->
        <path
          d="M68 50 L74 165 C74 171, 80 175, 100 175 C120 175, 126 171, 126 165 L132 50 Z"
          fill="rgba(255,255,255,0.25)"
          stroke="#C8B39B"
          stroke-width="2"
        />
        <!-- Clear Amber Cold Brew Liquid -->
        <path
          d="M69 65 L74 165 C74 170, 80 173, 100 173 C120 173, 126 170, 126 165 L131 65 Z"
          fill="#582C15"
        />
        <!-- Cinnamon stick (Thanh quế) poking out -->
        <rect
          x="114"
          y="32"
          width="7"
          height="85"
          rx="3.5"
          transform="rotate(18 114 32)"
          fill="#8B4219"
          stroke="#682F10"
          stroke-width="1.2"
        />
        <path d="M120 35 L128 85" stroke="#A85724" stroke-width="1" />
        <!-- Orange Slice (Lát cam vàng tươi) tucked in glass rim -->
        <g transform="translate(80, 52) rotate(-22)">
          <circle cx="0" cy="0" r="22" fill="#FFA500" stroke="#FF8C00" stroke-width="2.5" />
          <circle cx="0" cy="0" r="19" fill="#FFF3D1" />
          <!-- Orange pulp segments -->
          <path d="M0 0 L14 4 A16 16 0 0 0 11 -10 Z" fill="#FFA500" />
          <path d="M0 0 L4 14 A16 16 0 0 0 -10 11 Z" fill="#FFA500" />
          <path d="M0 0 L-14 -4 A16 16 0 0 0 -11 10 Z" fill="#FFA500" />
          <path d="M0 0 L-4 -14 A16 16 0 0 0 10 -11 Z" fill="#FFA500" />
        </g>
        <!-- Crystal Clear Ice cubes -->
        <rect
          x="85"
          y="85"
          width="20"
          height="20"
          rx="3"
          transform="rotate(12 85 85)"
          fill="rgba(255,255,255,0.4)"
          stroke="rgba(255,255,255,0.75)"
          stroke-width="1.5"
        />
        <rect
          x="92"
          y="125"
          width="18"
          height="18"
          rx="3"
          transform="rotate(-15 92 125)"
          fill="rgba(255,255,255,0.35)"
          stroke="rgba(255,255,255,0.75)"
          stroke-width="1.5"
        />
        <!-- Mint leaf garnish -->
        <path
          d="M102 42 C108 30, 120 32, 122 40 C116 45, 106 46, 102 42 Z"
          fill="#4B9344"
          stroke="#33672E"
          stroke-width="1"
        />
      </g>

      <!-- ============================================== -->
      <!-- 5. CÀ PHÊ ĐEN PHIN TRUYỀN THỐNG -->
      <!-- ============================================== -->
      <g v-else-if="type === 'black-coffee'">
        <!-- Traditional Glass cup bottom -->
        <path
          d="M72 105 L76 165 C76 170, 82 173, 100 173 C118 173, 124 170, 124 165 L128 105 Z"
          fill="rgba(255,255,255,0.3)"
          stroke="#C8B39B"
          stroke-width="2"
        />
        <!-- Deep black Robusta coffee in glass -->
        <path
          d="M74 125 L76 165 C76 169, 82 172, 100 172 C118 172, 124 169, 124 165 L126 125 Z"
          fill="#1C0E07"
        />
        <!-- Coffee drop falling -->
        <circle cx="100" cy="116" r="3" fill="#3D1C0C" />
        <!-- Aluminum Phin Saucer Plate (Đĩa phin nhôm) -->
        <ellipse
          cx="100"
          cy="104"
          rx="42"
          ry="6"
          fill="#D3D9DE"
          stroke="#A7B0B8"
          stroke-width="1.5"
        />
        <ellipse cx="100" cy="103" rx="38" ry="4.5" fill="#E8ECEF" />
        <!-- Phin Body (Thân phin) -->
        <path
          d="M78 52 L81 101 L119 101 L122 52 Z"
          fill="#D8DEE4"
          stroke="#9EA8B1"
          stroke-width="1.5"
        />
        <!-- Phin Rib rings -->
        <line x1="80" y1="72" x2="120" y2="72" stroke="#B0B9C1" stroke-width="1.5" />
        <line x1="80.5" y1="86" x2="119.5" y2="86" stroke="#B0B9C1" stroke-width="1.5" />
        <!-- Phin Lid (Nắp phin nhôm có núm cầm) -->
        <ellipse
          cx="100"
          cy="52"
          rx="23"
          ry="4"
          fill="#C4CCD3"
          stroke="#8E99A3"
          stroke-width="1.5"
        />
        <path
          d="M83 51 C83 45, 117 45, 117 51 Z"
          fill="#D8DEE4"
          stroke="#8E99A3"
          stroke-width="1.5"
        />
        <!-- Lid Knob -->
        <circle cx="100" cy="42" r="3.5" fill="#8E99A3" />
      </g>

      <!-- ============================================== -->
      <!-- 6. CÀ PHÊ SỮA ĐÁ SÀI GÒN -->
      <!-- ============================================== -->
      <g v-else-if="type === 'milk-coffee'">
        <!-- Classic Faceted Glass -->
        <path
          d="M70 48 L76 166 C76 171, 82 174, 100 174 C118 174, 124 171, 124 166 L130 48 Z"
          fill="rgba(255,255,255,0.3)"
          stroke="#C8B39B"
          stroke-width="2"
        />
        <!-- Condensed Milk Base -->
        <path
          d="M75 142 L76 166 C76 170, 82 172, 100 172 C118 172, 124 170, 124 166 L125 142 Z"
          fill="#FCEECA"
        />
        <!-- Swirled Iced Milk Coffee -->
        <path d="M70 50 L75 142 L125 142 L130 50 Z" fill="#884C23" />
        <!-- Cream ribbons / Swirl waves -->
        <path
          d="M74 95 Q100 120 126 95"
          stroke="#E2BF99"
          stroke-width="5"
          stroke-linecap="round"
          opacity="0.6"
        />
        <path
          d="M76 120 Q100 135 124 115"
          stroke="#FCEECA"
          stroke-width="4"
          stroke-linecap="round"
          opacity="0.6"
        />
        <!-- Top Foam head -->
        <ellipse cx="100" cy="50" rx="29" ry="6" fill="#B46E3A" stroke="#884C23" stroke-width="1" />
        <!-- Clear Ice cubes -->
        <rect
          x="80"
          y="65"
          width="18"
          height="18"
          rx="3"
          transform="rotate(16 80 65)"
          fill="rgba(255,255,255,0.4)"
          stroke="rgba(255,255,255,0.75)"
          stroke-width="1.2"
        />
        <rect
          x="98"
          y="88"
          width="17"
          height="17"
          rx="3"
          transform="rotate(-12 98 88)"
          fill="rgba(255,255,255,0.35)"
          stroke="rgba(255,255,255,0.75)"
          stroke-width="1.2"
        />
        <!-- Classic brown straw -->
        <path d="M116 28 L108 145" stroke="#4A2511" stroke-width="4.5" stroke-linecap="round" />
      </g>

      <!-- ============================================== -->
      <!-- 7. LATTE / CAPPUCCINO ART -->
      <!-- ============================================== -->
      <g v-else-if="type === 'latte' || type === 'cappuccino'">
        <!-- Saucer underneath -->
        <ellipse
          cx="100"
          cy="155"
          rx="55"
          ry="12"
          fill="#FAF6EE"
          stroke="#C8B39B"
          stroke-width="2"
        />
        <ellipse cx="100" cy="154" rx="52" ry="10" stroke="#C58940" stroke-width="1" fill="none" />
        <!-- Ceramic Cup -->
        <path
          d="M58 80 C58 135, 78 145, 100 145 C122 145, 142 135, 142 80 Z"
          fill="#FFFDF9"
          stroke="#C8B39B"
          stroke-width="2"
        />
        <!-- Handle -->
        <path
          d="M140 90 C154 90, 158 106, 158 116 C158 126, 148 130, 138 130"
          stroke="#FFFDF9"
          stroke-width="6"
          stroke-linecap="round"
          fill="none"
        />
        <path
          d="M140 90 C154 90, 158 106, 158 116 C158 126, 148 130, 138 130"
          stroke="#C8B39B"
          stroke-width="2"
          stroke-linecap="round"
          fill="none"
        />
        <!-- Cup Rim Oval with rich Crema -->
        <ellipse
          cx="100"
          cy="80"
          rx="42"
          ry="14"
          fill="#884C24"
          stroke="#FFFDF9"
          stroke-width="2"
        />
        <!-- Latte Art Rosette / Heart in Foam -->
        <ellipse cx="100" cy="80" rx="26" ry="9" fill="#FDF7EE" />
        <path d="M100 74 C92 70, 84 76, 100 86 C116 76, 108 70, 100 74 Z" fill="#FFFDF9" />
        <circle cx="94" cy="74" r="4" fill="#FFFDF9" />
        <circle cx="106" cy="74" r="4" fill="#FFFDF9" />
        <!-- Center line -->
        <path d="M100 71 L100 87" stroke="#884C24" stroke-width="1.5" stroke-linecap="round" />
        <!-- Cinnamon sprinkles for cappuccino -->
        <g v-if="type === 'cappuccino'">
          <circle cx="86" cy="81" r="1.2" fill="#753512" />
          <circle cx="114" cy="80" r="1.2" fill="#753512" />
          <circle cx="100" cy="73" r="1" fill="#753512" />
        </g>
      </g>

      <!-- ============================================== -->
      <!-- 8. MATCHA LATTE KEM PHÔ MAI -->
      <!-- ============================================== -->
      <g v-else-if="type === 'matcha'">
        <!-- Glass body -->
        <path
          d="M70 50 L76 165 C76 170, 82 174, 100 174 C118 174, 124 170, 124 165 L130 50 Z"
          fill="rgba(255,255,255,0.25)"
          stroke="#B3CDB0"
          stroke-width="2"
        />
        <!-- Vibrant Emerald Matcha layer -->
        <path
          d="M72 88 L76 165 C76 170, 82 173, 100 173 C118 173, 124 170, 124 165 L128 88 Z"
          fill="#4B853E"
        />
        <!-- Milk gradient swirl -->
        <path
          d="M74 125 Q100 145 124 125"
          stroke="#BFE0B4"
          stroke-width="5"
          stroke-linecap="round"
          opacity="0.6"
        />
        <!-- Thick Whipped Cream Cheese Cap -->
        <path
          d="M70 50 C70 50, 80 46, 100 46 C120 46, 130 50, 130 50 L128 88 C118 92, 105 88, 100 89 C95 90, 82 92, 72 88 Z"
          fill="#FFFDF8"
          stroke="#D3C9B6"
          stroke-width="1"
        />
        <ellipse cx="100" cy="49" rx="29" ry="5.5" fill="#FAF5E8" />
        <!-- Green matcha powder dusted on cream -->
        <circle cx="95" cy="49" r="1.8" fill="#386A2E" />
        <circle cx="105" cy="48" r="1.5" fill="#386A2E" />
        <circle cx="100" cy="51" r="1.2" fill="#386A2E" />
        <!-- Ice cubes -->
        <rect
          x="85"
          y="100"
          width="18"
          height="18"
          rx="3"
          transform="rotate(10 85 100)"
          fill="rgba(255,255,255,0.4)"
          stroke="rgba(255,255,255,0.7)"
          stroke-width="1.2"
        />
      </g>

      <!-- ============================================== -->
      <!-- 9. TRÀ ĐÀO / TRÀ TRÁI CÂY NHIỆT ĐỚI -->
      <!-- ============================================== -->
      <g v-else-if="type === 'fruit-tea' || type === 'peach-tea'">
        <!-- Curved Ice tea glass -->
        <path
          d="M70 45 L77 165 C77 170, 84 174, 100 174 C116 174, 123 170, 123 165 L130 45 Z"
          fill="rgba(255,255,255,0.3)"
          stroke="#E0BCAB"
          stroke-width="2"
        />
        <!-- Golden Amber Oolong Fruit Tea -->
        <path
          d="M71 58 L77 165 C77 170, 84 173, 100 173 C116 173, 123 170, 123 165 L129 58 Z"
          fill="#D87834"
        />
        <!-- Juicy Yellow Peach slices (Lát đào tươi) -->
        <g transform="translate(85, 75) rotate(-15)">
          <path
            d="M0 0 C15 -10, 25 15, 0 25 C-15 15, -10 -5, 0 0 Z"
            fill="#FFAF42"
            stroke="#FF7E26"
            stroke-width="1.5"
          />
          <path d="M0 2 C6 5, 8 16, 0 20" stroke="#FF5722" stroke-width="1.2" fill="none" />
        </g>
        <!-- Berries (Dâu tằm hoặc việt quất) -->
        <circle cx="112" cy="115" r="7" fill="#6A1B4D" stroke="#4A1035" stroke-width="1" />
        <circle cx="88" cy="135" r="6" fill="#881B52" stroke="#4A1035" stroke-width="1" />
        <!-- Mint sprig on rim -->
        <path
          d="M92 42 C85 30, 72 32, 70 40 C78 45, 88 45, 92 42 Z"
          fill="#4B9344"
          stroke="#33672E"
          stroke-width="1"
        />
        <!-- Clear ice cubes -->
        <rect
          x="88"
          y="90"
          width="18"
          height="18"
          rx="3"
          transform="rotate(18 88 90)"
          fill="rgba(255,255,255,0.45)"
          stroke="rgba(255,255,255,0.8)"
          stroke-width="1.4"
        />
        <!-- Clear straw -->
        <path d="M118 22 L110 145" stroke="#FF8A50" stroke-width="4.5" stroke-linecap="round" />
      </g>

      <!-- ============================================== -->
      <!-- 10. CROISSANT BƠ PHÁP NƯỚNG GIÒN -->
      <!-- ============================================== -->
      <g v-else-if="type === 'croissant'">
        <!-- Serving ceramic porcelain plate -->
        <ellipse
          cx="100"
          cy="142"
          rx="65"
          ry="18"
          fill="#FFFDF9"
          stroke="#D8C8B5"
          stroke-width="2"
        />
        <ellipse cx="100" cy="142" rx="60" ry="16" stroke="#C58940" stroke-width="1" fill="none" />
        <!-- Golden Crescent Croissant body -->
        <path
          d="M52 135 C50 100, 80 82, 100 82 C120 82, 150 100, 148 135 C138 142, 122 130, 100 130 C78 130, 62 142, 52 135 Z"
          fill="#E28E35"
          stroke="#9A5615"
          stroke-width="2"
        />
        <!-- Flaky pastry ridges & layers -->
        <path
          d="M72 102 C82 92, 118 92, 128 102"
          stroke="#9A5615"
          stroke-width="2.5"
          stroke-linecap="round"
          fill="none"
        />
        <path
          d="M80 114 C88 106, 112 106, 120 114"
          stroke="#9A5615"
          stroke-width="2.5"
          stroke-linecap="round"
          fill="none"
        />
        <!-- Golden butter glaze shine -->
        <path
          d="M85 92 Q100 86 115 92"
          stroke="#FFDF78"
          stroke-width="3"
          stroke-linecap="round"
          fill="none"
        />
        <circle cx="70" cy="120" r="1.5" fill="#753512" />
        <circle cx="130" cy="120" r="1.5" fill="#753512" />
      </g>

      <!-- ============================================== -->
      <!-- 11. BÁNH TIRAMISU CÀ PHÊ ESPRESSO -->
      <!-- ============================================== -->
      <g v-else-if="type === 'tiramisu'">
        <!-- Porcelain dessert plate -->
        <ellipse
          cx="100"
          cy="148"
          rx="62"
          ry="16"
          fill="#FFFDF9"
          stroke="#D8C8B5"
          stroke-width="2"
        />
        <!-- Tiramisu cake square slice -->
        <!-- Bottom ladyfinger soaked layer -->
        <polygon
          points="62,118 115,132 140,116 88,104"
          fill="#753F20"
          stroke="#542B14"
          stroke-width="1.5"
        />
        <!-- Middle Mascarpone cream layer -->
        <polygon
          points="62,106 115,120 140,104 88,92"
          fill="#FFF9E6"
          stroke="#D8C8B5"
          stroke-width="1.5"
        />
        <!-- Top Espresso soaked ladyfinger -->
        <polygon
          points="62,94 115,108 140,92 88,80"
          fill="#753F20"
          stroke="#542B14"
          stroke-width="1.5"
        />
        <!-- Top Mascarpone Cream dollops -->
        <polygon
          points="62,82 115,96 140,80 88,68"
          fill="#FFF9E6"
          stroke="#D8C8B5"
          stroke-width="1.5"
        />
        <!-- Cocoa powder dust on top surface -->
        <polygon points="62,82 115,96 140,80 88,68" fill="#582C15" opacity="0.85" />
        <!-- Cocoa speckles -->
        <circle cx="95" cy="82" r="1.5" fill="#3D1A0A" />
        <circle cx="105" cy="84" r="1.5" fill="#3D1A0A" />
        <circle cx="112" cy="78" r="1.2" fill="#3D1A0A" />
        <circle cx="85" cy="77" r="1.2" fill="#3D1A0A" />
        <!-- Chocolate stick & Mint leaf decoration on top -->
        <line
          x1="86"
          y1="72"
          x2="120"
          y2="60"
          stroke="#2B1408"
          stroke-width="3"
          stroke-linecap="round"
        />
        <path d="M102 65 C108 55, 118 56, 120 62 C114 66, 106 67, 102 65 Z" fill="#4B9344" />
      </g>

      <!-- ============================================== -->
      <!-- 12. MOUSSE CHANH LEO THANH MÁT (Cheesecake/Mousse) -->
      <!-- ============================================== -->
      <g v-else>
        <!-- Serving plate -->
        <ellipse
          cx="100"
          cy="150"
          rx="60"
          ry="16"
          fill="#FFFDF9"
          stroke="#D8C8B5"
          stroke-width="2"
        />
        <!-- Cake base crust -->
        <polygon
          points="60,126 122,136 142,118 82,108"
          fill="#C58940"
          stroke="#9A5615"
          stroke-width="1.5"
        />
        <!-- Velvet White Mousse cake body -->
        <polygon
          points="60,102 122,112 142,94 82,84"
          fill="#FFFFF5"
          stroke="#E2DACD"
          stroke-width="1.5"
        />
        <!-- Side face -->
        <polygon
          points="60,102 122,112 122,136 60,126"
          fill="#FFFDF0"
          stroke="#E2DACD"
          stroke-width="1.5"
        />
        <!-- Golden Yellow Passion Fruit Glaze Mirror on Top -->
        <polygon
          points="60,98 122,108 142,90 82,80"
          fill="#FFC72C"
          stroke="#FFA500"
          stroke-width="1.5"
        />
        <!-- Passionfruit seeds on glaze -->
        <ellipse cx="96" cy="94" rx="3.5" ry="2" transform="rotate(-15 96 94)" fill="#1A1105" />
        <ellipse cx="112" cy="98" rx="3" ry="1.8" transform="rotate(25 112 98)" fill="#1A1105" />
        <ellipse cx="120" cy="92" rx="2.8" ry="1.8" transform="rotate(-10 120 92)" fill="#1A1105" />
        <!-- Mint leaf garnish -->
        <path d="M85 82 C82 72, 70 74, 68 80 C75 84, 82 85, 85 82 Z" fill="#4B9344" />
      </g>
    </svg>
  </div>
</template>
