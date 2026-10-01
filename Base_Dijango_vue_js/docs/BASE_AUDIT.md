# Phase 0 — Base audit

Ngày khảo sát: 2026-09-18. Phạm vi khảo sát là repository hiện tại; chưa triển khai chức năng nghiệp vụ.

## Kết luận điều hành

Base có thể giữ lại phần lớn hạ tầng: Django modular monolith, PostgreSQL/Redis, JWT access token trong
memory, refresh token HttpOnly cookie, CSRF, response lỗi thống nhất, OpenAPI, Vue 3/Pinia/VeeValidate,
HTTP client chung, router guard, token CSS, unit/component test và CI. Không cần đổi stack hoặc viết lại
auth.

Base chưa phải sản phẩm quản lý quán cà phê. Chưa có role/quyền nghiệp vụ, đăng ký khách hàng, catalog,
kho, đơn hàng, thanh toán, ca, tài chính, đánh giá, recommendation, Excel, Three.js hoặc GSAP. Đây là phần
bổ sung theo từng vertical slice, không phải lỗi cần vá hàng loạt.

## Bằng chứng chạy thực tế

| Kiểm tra                | Kết quả  | Ghi chú                                                                  |
| ----------------------- | -------- | ------------------------------------------------------------------------ |
| Python / Node / uv      | Pass     | Python 3.12.10, Node 24.15.0, uv 0.8.22                                  |
| pnpm                    | Cảnh báo | Máy đang có pnpm 12.4.1; manifest khóa pnpm 11.19.0                      |
| Docker PostgreSQL/Redis | Pass     | Compose riêng `vubeo-coffee`, DB `vubeo_coffee`, host 5434/6381          |
| Ruff lint               | Pass     | `All checks passed`                                                      |
| Ruff format             | Fail     | 1 file test đang sửa trong working tree có line ending/format chưa chuẩn |
| Django check            | Pass     | Không có lỗi, 1 check được chủ động silence cho email login              |
| Migration check         | Pass     | Không phát hiện model change thiếu migration                             |
| Pytest                  | Pass     | 23/23 test                                                               |
| OpenAPI validation      | Pass     | `drf-spectacular --validate --fail-on-warn`                              |
| TypeScript              | Pass     | `vue-tsc -b`                                                             |
| ESLint                  | Pass     | 0 warning/error                                                          |
| Vitest                  | Pass     | 8 file, 10/10 test                                                       |
| Frontend build          | Pass     | 144 module; bundle JS khoảng 258 kB trước gzip                           |
| Prettier check          | Fail     | 59 file bị báo do checkout CRLF; chưa format hàng loạt                   |
| Playwright E2E          | Pass     | Auth/profile/logout: desktop Chromium và mobile Chromium, 2/2            |

Không chạy performance/load/security scanner. Chưa kiểm tra trình duyệt Safari/Firefox, thiết bị thật,
backup/restore, production deployment hoặc volume dữ liệu lớn.

## Ma trận hiện trạng

| Thành phần             | Hiện trạng                                         | Giữ/sửa/thêm              | Bằng chứng/file                  | Ưu tiên | Điều kiện hoàn thành                                |
| ---------------------- | -------------------------------------------------- | ------------------------- | -------------------------------- | ------- | --------------------------------------------------- |
| Repo/stack             | Monorepo Django + Vue                              | Giữ                       | `README.md`, ADR-001             | P0      | Lệnh local/CI đồng nhất                             |
| Backend architecture   | Modular monolith, view/serializer/service/selector | Giữ                       | `docs/standards/backend.md`      | P0      | App mới tuân thủ boundary                           |
| Database               | PostgreSQL 18; migration chuẩn                     | Giữ                       | `compose.yaml`, `pyproject.toml` | P0      | Schema domain + migration được review               |
| Redis                  | Cache/throttle                                     | Giữ                       | `config/settings/base.py`        | P1      | Prefix theo môi trường, health pass                 |
| Auth                   | JWT access memory + refresh cookie + CSRF          | Giữ, mở rộng              | ADR-004, accounts API            | P0      | Thêm registration/role mà không phá contract        |
| Role/permission        | Chỉ có Django flags; chưa có 3 role                | Thêm                      | `apps/accounts/models.py`        | P0      | Ma trận quyền BE + ownership test                   |
| Error contract         | `code/message/details/request_id`                  | Giữ                       | `common/exceptions.py`           | P0      | API mới dùng cùng contract                          |
| API docs               | drf-spectacular + snapshot                         | Giữ                       | `schema.yml`, CI                 | P0      | Mỗi endpoint có input/output/error chính            |
| Pagination/filter/sort | Chỉ pagination mặc định; chưa filter/sort contract | Bổ sung có kiểm soát      | settings + API standard          | P2      | Allowlist filter/sort từng endpoint                 |
| Upload/Excel           | Chưa có                                            | Thêm                      | Không có dependency/workflow     | P2      | Preview/confirm/idempotency/audit                   |
| Logging                | Request ID + structured format cơ bản              | Giữ, mở rộng audit log    | middleware/settings              | P0      | Không log secret; actor/action/object truy vết được |
| FE framework           | Vue 3 Composition API + strict TS                  | Giữ                       | `package.json`, ADR-003          | P0      | Module theo nghiệp vụ                               |
| Router/state           | Vue Router + Pinia                                 | Giữ, mở rộng              | router/store                     | P1      | Route meta role/permission + 403                    |
| API client             | Axios client, refresh single-flight                | Giữ                       | `src/lib/http/client.ts`         | P0      | Không tạo client thứ hai                            |
| Form validation        | VeeValidate + Zod                                  | Giữ                       | auth/profile                     | P1      | Schema dùng lại theo module                         |
| UI base                | Button/Input/Label/FormField/alert/toast/link      | Mở rộng                   | `src/components`                 | P1      | Showcase + trạng thái/a11y test                     |
| Design tokens          | Soft UI xanh dương, token còn ít                   | Sửa có kế thừa            | tokens + design-system doc       | P1      | Coffee designDNA, semantic token đầy đủ             |
| Responsive/a11y        | Mobile-first, focus, reduced-motion nền tảng       | Giữ, kiểm chứng sâu       | CSS/tests                        | P1      | 375/768/1024/1440 + keyboard/contrast               |
| Three.js/GSAP          | Chưa có dependency/asset                           | Thêm có điều kiện         | `package.json`                   | P1      | Lazy load, fallback, cleanup, no-motion             |
| Business modules       | Chưa có                                            | Thêm theo vertical slice  | chỉ có accounts/health           | P2+     | Mỗi slice đủ DB/BE/FE/test                          |
| CI                     | BE/FE quality gate; chưa E2E                       | Giữ, bổ sung              | `.github/workflows/ci.yml`       | P0/P11  | Formatter ổn định; E2E job quyết định rõ            |
| Local docs             | Khá đầy đủ cho base                                | Giữ, bổ sung product docs | README/standards                 | P0      | Một index kế hoạch không mâu thuẫn                  |

## Điểm giữ lại

- Tên thư mục `Base_dijango` để tránh churn đường dẫn.
- Django/DRF modular monolith; không thêm repository/controller/microservice.
- PostgreSQL làm nguồn sự thật; Redis chỉ hỗ trợ cache/throttle/lock có thể tái tạo.
- Auth cookie/access hiện tại, response lỗi, request ID và OpenAPI.
- Vue Composition API, Pinia, VeeValidate/Zod, Axios client chung và Tailwind 4.
- Base component hiện có và token semantic; mở rộng dần thay vì thay trắng.
- CI, pytest/Vitest/Playwright và lockfile hiện tại.

## Điểm phải sửa trước chức năng nghiệp vụ

1. Chốt và áp dụng line-ending/formatter nhất quán; không format trộn với feature.
2. Giải quyết working-tree change ở `test_auth_api.py` cùng chủ sở hữu trước khi commit Phase 0.
3. Đồng bộ pnpm local với `packageManager` 11.19.0 và tài liệu cách dùng Corepack trên Windows.
4. Chốt role, granular permission, ownership, state machine, money/inventory precision và idempotency.
5. Trả role/permissions cần thiết trong `/auth/me/`; thêm route guard và trang 403 sau khi BE có quyền.
6. Chốt thư viện Excel (`openpyxl` là đề xuất) và giới hạn file trước Phase 2.
7. Chốt dependency Three.js/GSAP, asset/license và performance budget trước khi cài ở Phase 1.
8. Tạo component showcase và hoàn thiện bộ custom component trước khi nhân rộng trang nghiệp vụ.

## Skill và design audit

Đã đọc và sử dụng `ui-ux-pro-max`. Truy vấn gợi ý glassmorphism, xanh lá/hồng và Fira Code; các phần đó
không được nhận nguyên xi vì lệch thương hiệu cà phê và giảm khả năng đọc ở POS. Phần được giữ là:
feedback cho thao tác async, semantic token, focus rõ, contrast, responsive table, reduced motion,
lazy-load, Three.js resource disposal và GSAP motion ngắn. DesignDNA đề xuất nằm ở `DESIGN_DNA.md`.

Không tìm thấy skill chuyên Three.js/GSAP/designDNA trong repository. Hướng dẫn Three.js và GSAP từ
UI/UX Pro Max chỉ dùng làm checklist; dependency chỉ được thêm sau khi Phase 1 bắt đầu.

## Rủi ro base

- Quyền mới có thể bị triển khai chỉ ở menu FE nếu không chốt permission service/BE từ Phase 0.
- Tồn kho và thanh toán cần idempotency/concurrency ngay từ schema; vá muộn sẽ khó giữ lịch sử.
- `User` đã có migration dùng chung; bổ sung role phải bằng migration mới, không sửa `0001_initial.py`.
- E2E hiện chỉ phủ auth. Các luồng tiền/kho phải có test tích hợp riêng.
- Formatter fail trên Windows có thể làm CI đỏ và sinh diff lớn nếu không tách sprint chuẩn hóa.
- Không có queue worker; import/recommendation/report v1 phải có giới hạn đồng bộ rõ, chỉ thêm background
  job khi số liệu thực tế chứng minh cần.
