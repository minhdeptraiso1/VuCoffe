# P01-S01 — Design tokens, components và showcase

**Trạng thái:** Done  
**Phase:** 1 — Design system, auth và layout

## Phạm vi đã triển khai

- Coffee semantic tokens, spacing, radius, shadow, z-index và motion.
- Primitive: button, input, textarea, select, checkbox.
- Surface/data/feedback: card, badge, alert, skeleton, empty state.
- Overlay: modal có Escape, backdrop close, focus trap và trả focus.
- File: upload shell kiểm tra giới hạn 5 MB, chưa nối API import.
- Các component được kiểm tra trực tiếp trong màn hình nghiệp vụ; route showcase `/design-system` đã gỡ
  theo quyết định sản phẩm vì không gọi API và không phục vụ người dùng cuối.

## Bằng chứng hiện tại

- Modal keyboard/focus và file size validation có Vitest; toàn frontend 13/13 test pass.
- Typecheck, ESLint, Prettier và production build pass.
- Playwright kiểm tra 375/768/1024/1440, mobile/desktop và reduced-motion: 6/6 pass.

## Chuyển tiếp sang Phase 2

- Table, pagination, filter bar và tabs tiếp tục được trích xuất khi catalog thật xuất hiện ở Phase 2,
  tránh tạo component giả không có use case.
- Drawer, confirm và upload shell đã có kiểm thử; import preview sẽ đi cùng API import thật.
