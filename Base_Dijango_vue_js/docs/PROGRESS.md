# Tiến độ triển khai

Ngày cập nhật: 2026-09-28.

## Trạng thái tổng

| Phase                             | Trạng thái  | Ghi chú                                                   |
| --------------------------------- | ----------- | --------------------------------------------------------- |
| Phase 0 — Audit và chuẩn hóa base | Complete    | P00-S01/S02/S03 đạt toàn bộ gate                          |
| Phase 1 — Design/auth/layout      | Complete    | P01-S01/S02/S03 đạt gate và có E2E ba vai trò             |
| Phase 2 — Menu và dữ liệu nền     | In review   | Luồng chính chạy; còn đóng các gap Excel/E2E ghi bên dưới |
| Phase 3–11                        | Not started | Chờ bắt đầu nghiệp vụ kho                                 |

## Hoàn thành

- P00-S01: đọc base/docs/source/CI/dependencies và skill UI/UX.
- Chạy backend checks/test/OpenAPI, frontend typecheck/lint/test/build và E2E auth desktop/mobile.
- Tạo scope, audit, designDNA đề xuất, architecture, component/Excel spec, decisions và roadmap.
- P00-S02: chuẩn LF/formatter, pnpm 11.19.0/Corepack, tài liệu Windows và toàn bộ quality gate.
- Compose project riêng `vubeo-coffee`, database `vubeo_coffee`, PostgreSQL 5434, Redis 6381 và volume mới.
- P00-S03: khóa role/duty permission, decimal precision, state/ledger/idempotency và Excel contract.
- P01-S01: coffee tokens và bộ component dùng chung primitive/surface/feedback/modal/file.
- P01-S02: role migration, registration, enriched session contract, admin employee permission API,
  role guard, 403 và ba layout theo vai trò.
- P01-S03: landing content-first, GSAP scroll/depth nhẹ, ảnh sticky/crossfade, reduced-motion và cleanup.
- Landing 3D phản ứng theo scroll, GSAP reveal theo viewport; toast auth và confirm form dùng chung.
- Đồng bộ header dùng chung cho trang chủ, thực đơn và khu vực khách hàng; điều hướng desktop giữ một
  hàng, mobile dùng menu thu gọn và các liên kết section hoạt động qua hash route.
- Khu vực quản trị/nhân viên đã chuyển sang management shell chuyên nghiệp với sidebar trái trên desktop,
  drawer trên mobile, topbar ngữ cảnh và dashboard tiếng Việt theo đúng vai trò.
- Gỡ route/showcase nội bộ `/design-system` khỏi sản phẩm; hệ token và component dùng chung vẫn được giữ.
- Migration local tạo ba tài khoản test role admin/employee/customer với password `123456`.
- Backend Phase 1 Done: employee list pagination, assignable permission catalog, grant/revoke validation,
  coarse-role enforcement và OpenAPI đã hoàn chỉnh.
- Backend 30/30 test, coverage 92%, Ruff/check/migration/OpenAPI pass.
- Frontend 30/30 Vitest, typecheck/lint/build; 12/12 kịch bản public/menu desktop-mobile và 4/4
  kịch bản auth/ba vai trò với backend thật pass.
- P02-S01: catalog thật gồm danh mục, món, biến thể, topping, allowlist, lịch sử giá, optimistic lock,
  API quản trị và màn quản lý tiếng Việt.
- P02-S02: public menu/search/filter, focal point ảnh, menu giấy editorial, custom select, modal tùy chỉnh
  component hóa và endpoint xác nhận option/giá phía server.
- P02-S03: đơn vị/quy đổi có chặn vòng lặp, nguyên liệu, nhà cung cấp, công thức versioned và màn quản lý.
- P02-S03 UX bổ sung trình chỉnh sửa quy đổi đơn vị và trình tạo công thức theo món → kích cỡ → nhiều
  nguyên liệu; đơn vị định lượng lấy từ hồ sơ nguyên liệu, chặn nguyên liệu trùng và payload không cần
  nhập ngày hiệu lực thủ công.
- P02-S04: XLSX template → preview → confirm idempotent → history, mode create/update/upsert,
  stale dependency check, file lỗi, export và formula-injection defense.
- P02-S04 UX/file v2: header tiếng Việt, dấu `(*)` cho trường bắt buộc, dropdown DB cho danh mục/đơn vị,
  dropdown Có/Không; file export dùng lại đúng contract template để chỉnh sửa rồi import lại.
- Backend Phase 2: 43/43 test pass; Ruff, migration check và OpenAPI pass.
- Frontend Phase 2: 33/33 Vitest, typecheck, lint, production build và 4/4 E2E menu desktop/mobile
  pass với backend SQLite tạm; Docker/PostgreSQL E2E cần chạy lại khi Docker Desktop hoạt động.

## Còn lại trước khi khóa Phase 2

- Tên/logo chính thức chưa có; đang dùng text mark `Kim Thành Coffee` và font fallback.
- Data-heavy primitive được trích xuất cùng catalog thật ở Phase 2, tránh abstraction giả.
- Lighthouse/device thật chuyên sâu vẫn nằm ở Phase 11; route landing hiện không tải Three.js chunk.
- Excel hiện hỗ trợ danh mục, món bán, nguyên liệu và nhà cung cấp. Cần thêm adapter cho biến thể, món
  thêm, đơn vị và quy đổi; hoàn thiện đúng semantics update ô trống/`__CLEAR__` và validation kiểu dữ liệu.
- Cần E2E Excel create/update/error theo DoD P02-S04 và chạy lại full-stack bằng PostgreSQL/Docker.
- Đã khóa PROD-020 và `INVENTORY_REPLENISHMENT.md`: recipe là tiêu hao chuẩn, không phải tồn vật lý;
  Phase 3 tách tồn ước tính/kiểm kê và P08-S04 mới triển khai đề xuất nhập có loss/yield.

## Task tiếp theo được phép bắt đầu

Đóng gap `P02-S04` ở trên; sau đó mới bắt đầu `P03-S01` — nhập hàng, lô tồn và sổ kho append-only.

## Quy tắc cập nhật

Sau mỗi sprint: cập nhật status, task IDs hoàn thành, migration/API/UI đã giao, lệnh kiểm tra và kết quả,
blocker/known issue, task sớm nhất đủ dependency. Không đánh dấu Done nếu còn mock thay API thật.
