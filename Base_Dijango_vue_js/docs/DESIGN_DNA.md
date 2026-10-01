# DesignDNA đề xuất — VuBeo Coffee

Trạng thái: đề xuất cho Phase 1, chưa áp dụng vào source. Base hiện có Soft UI xanh dương trong
`frontend/docs/design-system.md`; Phase 1 sẽ migrate token có kiểm soát, không đổi trắng UI trong Phase 0.

## Tính cách thương hiệu

Ấm, thủ công, nhanh và đáng tin. Customer UI gợi cảm giác cà phê mới pha; POS/admin ưu tiên độ rõ, tốc
độ thao tác và mật độ dữ liệu. Tránh “luxury tối khó đọc”, glassmorphism dày, neon, gradient tím và animation
trang trí liên tục.

## Màu semantic

| Token                    | Light đề xuất | Mục đích                  |
| ------------------------ | ------------- | ------------------------- |
| `--color-bg`             | `#F7F3EC`     | Nền cream                 |
| `--color-surface`        | `#FFFCF7`     | Card/form                 |
| `--color-surface-strong` | `#F0E6D7`     | Panel phân cấp            |
| `--color-text`           | `#2B2118`     | Chữ chính espresso        |
| `--color-text-muted`     | `#6F6256`     | Chữ phụ, đạt contrast     |
| `--color-border`         | `#D8C8B5`     | Border/divider            |
| `--color-primary`        | `#6F3F25`     | CTA/chủ đạo coffee brown  |
| `--color-primary-hover`  | `#57301D`     | Hover                     |
| `--color-primary-soft`   | `#EAD8C6`     | Selected/subtle           |
| `--color-accent`         | `#B85C38`     | Copper, CTA phụ/điểm nhấn |
| `--color-success`        | `#2F6B45`     | Thành công/còn hàng       |
| `--color-warning`        | `#9A650D`     | Cảnh báo                  |
| `--color-error`          | `#A63D40`     | Lỗi/destructive           |
| `--color-info`           | `#315E7A`     | Thông tin                 |
| `--color-focus`          | `#1F6FEB`     | Focus ring dễ nhận biết   |

Các màu trạng thái luôn đi kèm icon/text. Dark mode không thuộc MVP trừ khi người dùng mở phạm vi; token
vẫn đặt semantic để có thể map sau này. Contrast mục tiêu WCAG AA: chữ thường ≥4.5:1, UI/large text ≥3:1.

## Typography

- Heading đề xuất: `Fraunces` hoặc serif có giấy phép phù hợp, chỉ cho hero/section/customer marketing.
- Body/UI/POS/admin: `Inter` và system sans đang có; số dùng tabular numerals trong tiền/báo cáo.
- Nếu chưa duyệt webfont/hosting, Phase 1 giữ Inter/system để không chặn render.
- Scale: 12/14/16/18/24/32/40/56 px; body mobile 16 px; line-height body 1.5.
- Không dùng monospace cho heading đại trà; gợi ý Fira Code từ skill bị loại vì tạo cảm giác kỹ thuật.

## Spacing, grid và container

- Nhịp 4/8 px: 4, 8, 12, 16, 24, 32, 48, 64.
- Customer container tối đa 1200 px; content reading 680–760 px.
- Admin/POS có density mode chuẩn 8–24 px, không giảm control dưới 44 px.
- Breakpoint kiểm chứng: 375, 768, 1024, 1440 px.
- Table mobile: ưu tiên horizontal scroll có header/context hoặc card projection; không bóp cột mất nghĩa.

## Shape, border, elevation

- Radius: control 8 px, card 12 px, modal 16 px, pill chỉ cho badge/chip.
- Border 1 px semantic; shadow nhẹ, không dùng neumorphism làm giảm contrast.
- Z-index scale: base 0, sticky 10, dropdown 20, overlay 30, modal 40, toast 50.
- Overlay scrim 45–55% đen; modal giữ focus trap và trả focus về trigger.

## Icon và hình ảnh

- Chọn một bộ SVG hỗ trợ Vue sau khi kiểm tra dependency/license; không dùng emoji làm icon thao tác.
- Icon 16/20/24 px, stroke nhất quán; icon-only control có label và hit area ≥44×44 px.
- Ảnh đồ uống có tỉ lệ nhất quán, alt text, lazy-load, fallback và không làm thay đổi layout.
- Asset 3D phải liên quan cà phê, có quyền sử dụng, có budget dung lượng và ảnh poster fallback.

## Interaction states

Mọi control có default, hover, active, focus-visible, disabled, loading và error/success nếu phù hợp.
Loading >300 ms phải có feedback; submit bị disable/idempotent để tránh double click. Empty state nêu hành động
tiếp theo. Error không chỉ nói “có lỗi”, phải có cách khắc phục và request ID khi là lỗi server.

## Motion

- Micro interaction 150–250 ms; enter 220–350 ms; exit ngắn hơn enter.
- Customer landing có thể dùng GSAP reveal nhỏ 8–16 px; tối đa 8 item/stagger group.
- POS/admin không animate row/table liên tục; transition không chặn click/navigation.
- `prefers-reduced-motion` là reactive; kill timeline/ScrollTrigger khi unmount.
- Không để content mặc định invisible nếu JS/GSAP lỗi.

## Hero có chiều sâu theo scroll

- Chỉ ở customer home/hero; dùng GSAP transform nhẹ theo scroll trên ảnh tĩnh có mask/feather.
- Ảnh và CTA render ngay; motion chỉ tăng chiều sâu, không phải điều kiện để đọc hoặc đặt món.
- Cleanup ScrollTrigger khi unmount; reduced motion không tải GSAP.
- Không dùng WebGL/Three.js trên critical landing route, POS hay admin.

## Áp dụng theo bề mặt

| Bề mặt   | Hướng                                                                                         |
| -------- | --------------------------------------------------------------------------------------------- |
| Customer | Ấm, ảnh món rõ, khoảng thở lớn, CTA đặt món nổi bật, motion/3D có fallback                    |
| POS      | Mật độ cao vừa phải, touch target lớn, giỏ luôn nhìn thấy, status/total rõ, keyboard-friendly |
| Barista  | Hàng đợi theo trạng thái/thời gian, màu chỉ hỗ trợ chứ không thay text, cập nhật nhanh        |
| Admin    | Sidebar rõ, table/filter/bulk action nhất quán, chart hạn chế và có bảng thay thế             |

## Gate Phase 1

- Component được kiểm chứng qua unit test và màn hình nghiệp vụ thật; không mở showcase cho người dùng.
- Contrast, keyboard, focus order, reduced motion và screen reader label được kiểm tra.
- So sánh visual ở 375/768/1024/1440 px.
- GSAP có fallback, lazy chunk, cleanup test/manual proof và không ảnh hưởng luồng đặt món.
- Design token mới được ghi vào source of truth; tài liệu base cũ được cập nhật thay vì để hai nguồn mâu thuẫn.
