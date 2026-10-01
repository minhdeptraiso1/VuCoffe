# P01-S03 — Customer home, Three.js và GSAP

**Trạng thái:** Done  
**Phase:** 1 — Design system, auth và layout

## Đã triển khai

- Landing semantic, mobile-first; CTA dùng link thật và không phụ thuộc WebGL.
- Banner ảnh thật có feather hai lớp, không lộ khung; GSAP tạo chiều sâu 3D nhẹ theo scroll mà không
  thêm WebGL vào critical route.
- Bốn chương rang mộc dùng ảnh sticky/crossfade; bước 4 có vùng giữ riêng để nội dung xuất hiện đầy đủ
  trước khi ảnh rời section.
- GSAP dynamic import; nội dung và ảnh tĩnh luôn hiển thị trước, là fallback khi motion bị tắt.
- GSAP ScrollTrigger reveal từng chương khi vào viewport, không pin hoặc chiếm quyền native scroll.
- Reduced-motion không tải motion; không có RAF/WebGL/GPU loop trên route hiện tại.
- GSAP context được revert khi rời route.
- Toast dùng chung cho login/register/logout/profile; confirm dialog dùng form semantic, focus trap và loading.

## Bằng chứng

- Production build chỉ tải ScrollTrigger khoảng 18 KB gzip; không phát sinh Three.js chunk trên route.
- Playwright landing desktop/mobile và 4 breakpoint/reduced-motion: pass.
- Typecheck, ESLint, Vitest và build: pass.

## Kết luận performance

- Không còn WebGL trong critical landing bundle. Responsive/reduced-motion và cleanup đã có E2E; audit
  Lighthouse sâu trên thiết bị thật được giữ ở Phase 11, không chặn catalog Phase 2.
