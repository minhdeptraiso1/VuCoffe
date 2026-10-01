# Implementation plan end-to-end

Kế hoạch cho một full-stack developer, effort là ngày công tập trung, không phải ngày lịch; không gồm thời
gian chờ duyệt, tạo asset, UAT hoặc thay đổi phạm vi. Mỗi sprint chỉ Done khi DB + BE + FE + API thật +
test/tài liệu liên quan hoàn chỉnh. Task ID: `P<phase>-S<sprint>-<area><number>`.

## Thứ tự và dependency

Phase 0 → 1 → 2 → 3 → 4 → 5 → 6/7 → 8 → 9 → 10 → 11. Phase 6 và phần đầu Phase 7 có thể đổi
thứ tự sau khi Phase 5 ổn định, nhưng một developer không nên chạy song song. Event recommendation được
thu từ Phase 2/4/6 dù engine nằm ở Phase 9. Cost snapshot được thu từ Phase 3/5 dù báo cáo ở Phase 8/10.

## Definition of Ready chung

- Dependency sprint trước đạt gate; decision/schema/API contract liên quan được duyệt.
- Working tree được kiểm tra và thay đổi người dùng được bảo toàn.
- Có happy path, error/permission/concurrency case và dữ liệu demo dự kiến.
- Asset/license/dependency mới được xác minh trước khi thêm.

## Definition of Done chung

- Migration mới (nếu có) được review; không sửa migration đã áp dụng.
- BE permission/ownership/validation/transaction/idempotency đúng; OpenAPI cập nhật.
- FE dùng component/designDNA, API thật, loading/empty/error/validation/responsive/a11y.
- Test rủi ro chính pass; lint/format/check/build pass; E2E khi đổi luồng tích hợp.
- Tài liệu/`PROGRESS.md`/decision được cập nhật; demo evidence và known issue được ghi.

---

## Phase 0 — Audit và chuẩn hóa base

### P00-S01 — Audit và kế hoạch (đã hoàn thành) — 2–3 ngày công

1. **Mục tiêu:** xác minh base và tạo source of truth cho sản phẩm.
2. **Dependency/Ready:** repository clone được; đọc toàn bộ AGENTS/standards.
3. **Thứ tự:** audit docs/source → chạy gate → design/architecture decisions → roadmap.
4. **DB `P00-S01-DB01`:** đọc migration/settings/compose; không đổi schema.
5. **BE `P00-S01-BE01`:** audit auth/error/OpenAPI/test/module boundary.
6. **FE `P00-S01-FE01`:** audit router/state/client/components/tokens/a11y/toolchain.
7. **API `P00-S01-API01`:** ghi contract hiện hành và state-machine mục tiêu.
8. **Excel `P00-S01-XL01`:** thiết kế preview/confirm/export contract, chưa thêm dependency.
9. **Happy/error:** gate chạy thật; lỗi formatter được ghi, không tuyên bố pass giả.
10. **Acceptance:** các tài liệu Phase 0 tồn tại, có bằng chứng file/lệnh và scope rõ.
11. **DoD:** không có code nghiệp vụ/migration/dependency mới.
12. **Demo/evidence:** 23 pytest, 10 Vitest, build, 2 Playwright pass; audit table.
13. **Rủi ro/out:** chưa test production/performance/backup/device thật.
14. **Effort:** 2–3 ngày.

### P00-S02 — Tooling và base normalization — 2–4 ngày công

1. **Mục tiêu:** quality gate local/CI ổn định trên Windows và Linux.
2. **Dependency/Ready:** duyệt cách xử lý working-tree change hiện có; không trộn feature.
3. **Thứ tự:** line ending → pnpm/Corepack → formatter → smoke/E2E docs.
4. **DB `P00-S02-DB01`:** xác minh `.env.example`, test DB/Redis port; không reset volume.
5. **BE `P00-S02-BE01`:** xử lý format test hiện có, rà command `uv` Windows.
6. **FE `P00-S02-FE01`:** chuẩn CRLF/LF và pnpm 11.19.0; không reformat vô nghĩa ngoài commit riêng.
7. **API `P00-S02-API01`:** schema snapshot không đổi ngoài line ending.
8. **Excel `P00-S02-XL01`:** chưa áp dụng.
9. **Happy/error:** clone sạch chạy đủ gate; Corepack/cache/network lỗi có hướng dẫn.
10. **Acceptance:** Ruff/Prettier và toàn CI commands pass; E2E auth reproducible.
11. **DoD:** diff normalization tách biệt, README chính xác, không đổi runtime behavior.
12. **Demo/evidence:** log local + CI, `git diff` sạch sau generate schema.
13. **Rủi ro/out:** không nâng major dependency trong sprint này.
14. **Effort:** 2–4 ngày.

### P00-S03 — Contract nền domain/quyền/concurrency — 3–5 ngày công

1. **Mục tiêu:** khóa decision chặn schema trước khi viết feature.
2. **Dependency/Ready:** P00-S02; duyệt mục Proposed trong `DECISIONS.md`.
3. **Thứ tự:** role matrix → decimal/state/ledger/idempotency → API/filter/audit convention.
4. **DB `P00-S03-DB01`:** ERD logical, naming/index/soft-delete/immutable policy; chưa tạo bảng business.
5. **BE `P00-S03-BE01`:** permission naming, transition/service/locking test patterns.
6. **FE `P00-S03-FE01`:** route meta/permission contract, error 409 và stale-state UX.
7. **API `P00-S03-API01`:** action endpoint, pagination/filter/order/idempotency header convention.
8. **Excel `P00-S03-XL01`:** duyệt openpyxl, limit, template version, blank/clear semantics.
9. **Happy/error:** mô phỏng cancel/paid/reserve/consume/double-confirm trên state table.
10. **Acceptance:** không còn decision mâu thuẫn ảnh hưởng migration Phase 1–3.
11. **DoD:** ADR/product docs cập nhật; checklist review được ký duyệt.
12. **Demo/evidence:** walkthrough ERD/state/permission/import sequence.
13. **Rủi ro/out:** chưa tạo UI/business API.
14. **Effort:** 3–5 ngày.

---

## Phase 1 — Design system, auth và layout

### P01-S01 — Design tokens, custom components và showcase — 6–9 ngày công

1. **Mục tiêu:** hệ component đủ dùng trước khi nhân rộng màn hình.
2. **Dependency/Ready:** Phase 0; brand name/logo/icon/font license được duyệt hoặc dùng fallback.
3. **Thứ tự:** token → primitive → overlay/data/file components → showcase → a11y test.
4. **DB `P01-S01-DB01`:** không đổi DB.
5. **BE `P01-S01-BE01`:** không API mới; giữ error payload làm fixture contract.
6. **FE `P01-S01-FE01..06`:** migrate token coffee; button/input/select/etc.; modal/drawer/table;
   feedback/file components; showcase; responsive/keyboard tests.
7. **API `P01-S01-API01`:** component error/loading nhận `AppError`, không hardcode transport.
8. **Excel `P01-S01-XL01`:** shell `AppFileUpload/AppImportPreview/AppExportAction`, chưa nối import.
9. **Happy/error:** all states, long text, focus trap, escape, disabled/loading, empty/error.
10. **Acceptance:** trang nghiệp vụ có thể xây mà không tạo control/card/table ad hoc.
11. **DoD:** showcase + Vitest + visual checklist 4 breakpoint/reduced motion pass.
12. **Demo/evidence:** quay/ảnh showcase và keyboard traversal.
13. **Rủi ro/out:** không đổi mọi page cũ trong một commit; chưa Three.js.
14. **Effort:** 6–9 ngày.

### P01-S02 — Registration, role/permission và layouts — 7–10 ngày công

1. **Mục tiêu:** ba role đăng nhập đúng surface và BE enforce quyền.
2. **Dependency/Ready:** P01-S01; role decision khóa.
3. **Thứ tự:** role migration/data migration → registration/me contract → permission guards → layouts/403.
4. **DB `P01-S02-DB01..02`:** migration role group/seed permissions; không sửa accounts 0001.
5. **BE `P01-S02-BE01..04`:** customer registration, `/me` role/permission, admin employee grant,
   permission/ownership helpers và tests.
6. **FE `P01-S02-FE01..04`:** register page; auth types/store; role-aware route guard/403; customer,
   employee, admin shells.
7. **API `P01-S02-API01`:** `POST /auth/register/`, enriched `GET /auth/me/`, employee permission API.
8. **Excel `P01-S02-XL01`:** không import user/password; employee bulk import ngoài MVP.
9. **Happy/error:** duplicate email, inactive user, forbidden route/API, revoked permission mid-session.
10. **Acceptance:** role không chỉ ẩn menu; API trả 403 đúng, customer chỉ thấy dữ liệu của mình.
11. **DoD:** migration, OpenAPI, BE/FE/E2E 3 role pass.
12. **Demo/evidence:** register customer; employee bị chặn/admin cấp quyền; admin layout.
13. **Rủi ro/out:** không MFA/social login/password reset nếu chưa mở scope.
14. **Effort:** 7–10 ngày.

### P01-S03 — Customer home và GSAP scroll depth — 4–7 ngày công

1. **Mục tiêu:** landing đúng thương hiệu, motion có chiều sâu và không chặn chuyển đổi.
2. **Dependency/Ready:** P01-S01; asset/license/performance budget được duyệt.
3. **Thứ tự:** static hero → GSAP depth/reveal → fallback/cleanup/perf.
4. **DB `P01-S03-DB01`:** không đổi DB.
5. **BE `P01-S03-BE01`:** health/public config tối thiểu chỉ nếu thực sự cần.
6. **FE `P01-S03-FE01..04`:** semantic landing; ảnh thật có feather; scoped GSAP depth/crossfade;
   reduced-motion.
7. **API `P01-S03-API01`:** không phụ thuộc menu mock; CTA có thể tới empty/menu placeholder rõ.
8. **Excel:** không áp dụng.
9. **Happy/error:** asset fail, JS disabled-ish fallback, reduced motion, route unmount.
10. **Acceptance:** CTA/menu không phụ thuộc motion; không leak ScrollTrigger/listener; no-motion không autoplay.
11. **DoD:** bundle split, responsive/reduced-motion E2E, Vitest và cleanup proof.
12. **Demo/evidence:** network lazy chunk, fallback screenshot, reduced-motion test.
13. **Rủi ro/out:** không motion trang trí ở POS/admin; không dùng model/asset chưa rõ license.
14. **Effort:** 4–7 ngày.

---

## Phase 2 — Menu và dữ liệu nền

### P02-S01 — Catalog core và quản trị — 7–10 ngày công

1. **Mục tiêu:** admin quản lý category/product/variant/topping/price/availability.
2. **Dependency/Ready:** Phase 1; stable-code/price decisions khóa.
3. **Thứ tự:** schema/migration → service/API → admin pages → contract/test.
4. **DB `P02-S01-DB01..03`:** Category, Product, Variant, Topping, allowlist, price/effective history,
   constraints/indexes/codes.
5. **BE `P02-S01-BE01..04`:** CRUD/service/selectors, filter/sort/page, permission, deactivate rules.
6. **FE `P02-S01-FE01..04`:** list/filter/table, create/edit forms, variant/topping editor, status/error.
7. **API `P02-S01-API01`:** `/categories/`, `/products/`, `/variants/`, `/toppings/`; decimal string.
8. **Excel `P02-S01-XL01`:** chỉ xác định column dictionary; platform import ở S04.
9. **Happy/error:** duplicate code, invalid price window, deactivate referenced item, stale edit 409.
10. **Acceptance:** catalog thật quản trị được; lịch sử order tương lai không phụ thuộc tên/giá live.
11. **DoD:** migration/OpenAPI/permission/service/API/component tests pass.
12. **Demo/evidence:** admin tạo món nhiều size/topping, filter và deactivate.
13. **Rủi ro/out:** chưa recipe/stock/customer checkout.
14. **Effort:** 7–10 ngày.

### P02-S02 — Customer menu và product customization — 5–8 ngày công

1. **Mục tiêu:** khách xem/tìm/lọc món và cấu hình lựa chọn hợp lệ.
2. **Dependency/Ready:** P02-S01; images/fallback policy.
3. **Thứ tự:** public selectors/API → menu/detail UI → option validation → analytics hooks.
4. **DB `P02-S02-DB01`:** image metadata/display order/tag nếu được duyệt; migration nhỏ.
5. **BE `P02-S02-BE01..03`:** public available catalog, search/filter, detail option matrix/cache policy.
6. **FE `P02-S02-FE01..04`:** menu cards/skeleton/empty, detail drawer/page, size/topping/sugar/ice form,
   responsive/accessibility.
7. **API `P02-S02-API01`:** read-only `/menu/` và `/menu/{slug}/`; không expose admin-only fields.
8. **Excel:** không import ở customer UI.
9. **Happy/error:** unavailable/deactivated item, invalid combination, image fail, network/empty search.
10. **Acceptance:** customization payload được server validate; không dùng mock catalog.
11. **DoD:** API/Vitest/E2E browse menu; loading/empty/error và keyboard pass.
12. **Demo/evidence:** mobile/desktop menu, search/filter và option price update.
13. **Rủi ro/out:** chưa đặt order; availability nguyên liệu chỉ thêm sau Phase 3.
14. **Effort:** 5–8 ngày.

### P02-S03 — Ingredient, unit, supplier và recipe — 8–12 ngày công

1. **Mục tiêu:** master data và định lượng chuẩn đủ cho reservation, standard COGS và dự báo nhu cầu;
   recipe không được xem là số lượng vật lý chính xác tuyệt đối.
2. **Dependency/Ready:** P02-S01; unit precision/lot/FEFO decision.
3. **Thứ tự:** units/conversion → ingredients/suppliers → recipes → admin UI/test.
4. **DB `P02-S03-DB01..04`:** Unit, conversion constraints, Ingredient, Supplier, Recipe/RecipeItem,
   effective/version and indexes.
5. **BE `P02-S03-BE01..04`:** CRUD, conversion cycle/precision validation, recipe version service,
   permissions/selectors.
6. **FE `P02-S03-FE01..04`:** lists/forms, conversion editor, recipe builder, validation summaries.
7. **API `P02-S03-API01`:** `/units/`, `/ingredients/`, `/suppliers/`, `/recipes/`.
8. **Excel `P02-S03-XL01`:** dictionary/template inputs for S04.
9. **Happy/error:** cyclic conversion, duplicate base unit, missing ingredient, negative/zero recipe qty.
10. **Acceptance:** mỗi sellable variant/topping có recipe version hoặc explicit no-stock flag; tài liệu
    phân biệt tiêu hao chuẩn với tồn kiểm kê thực tế.
11. **DoD:** migration, decimal/conversion/permission tests, API + UI thật pass.
12. **Demo/evidence:** tạo nguyên liệu g/ml, supplier, recipe một ly và version mới.
13. **Rủi ro/out:** chưa tồn/receipt; không tự sửa recipe history.
14. **Effort:** 8–12 ngày.

### P02-S04 — Excel foundation và master-data import/export — 8–12 ngày công

1. **Mục tiêu:** workflow template→preview→confirm→history cho master data.
2. **Dependency/Ready:** P02-S01/S03; `IMPORT_EXPORT_SPEC.md` duyệt.
3. **Thứ tự:** dependency/model/job → parser/validator → API → preview UI → module adapters.
4. **DB `P02-S04-DB01..02`:** ImportJob, RowIssue, artifact metadata/hash/idempotency/index.
5. **BE `P02-S04-BE01..05`:** safe XLSX reader, template/version, preview, confirm/revalidate, export.
6. **FE `P02-S04-FE01..04`:** upload wizard, preview/error filter, confirm/result/history/download.
7. **API `P02-S04-API01`:** import endpoints theo spec; export dùng same filter và full result.
8. **Excel `P02-S04-XL01..04`:** catalog/ingredient/supplier templates và formula-injection defense.
9. **Happy/error:** duplicate, blank/clear, stale confirm, double confirm, limit, permission revoke.
10. **Acceptance:** file lỗi ghi 0 row; confirm không lặp; không chỉnh stock qua ingredient import.
11. **DoD:** transaction/idempotency/security tests + FE E2E một create/update/error case.
12. **Demo/evidence:** tải template, preview new/update/error, confirm và history.
13. **Rủi ro/out:** document import/background jobs chưa làm.
14. **Effort:** 8–12 ngày.

---

## Phase 3 — Nhập kho và tồn ban đầu

### P03-S01 — Receipt, lot và posting — 8–12 ngày công

1. **Mục tiêu:** phiếu nhập draft/approve/post tạo tồn và lot audit được.
2. **Dependency/Ready:** Phase 2; lot/expiry/cost decision khóa.
3. **Thứ tự:** receipt/lot schema → draft UI → approval/post transaction → history/test.
4. **DB `P03-S01-DB01..03`:** StockReceipt/Line, InventoryLot, StockMovement append-only, status events.
5. **BE `P03-S01-BE01..05`:** CRUD draft, submit/approve/post lock, totals/cost, permissions, immutable posted.
6. **FE `P03-S01-FE01..04`:** receipt list/form, line editor, approval detail, posting result.
7. **API `P03-S01-API01`:** receipt CRUD/action endpoints; 409 stale state.
8. **Excel `P03-S01-XL01`:** chưa import; chuẩn column dictionary.
9. **Happy/error:** duplicate supplier ref, expiry invalid, post twice, edit posted, permission denied.
10. **Acceptance:** posting tạo đúng lot/movement một lần; on-hand đối chiếu được.
11. **DoD:** concurrency/rollback/permission tests + UI/API integration.
12. **Demo/evidence:** draft→approve→post và xem movement/lot.
13. **Rủi ro/out:** không supplier debt; payment supplier ở Phase 7.
14. **Effort:** 8–12 ngày.

### P03-S02 — Availability, ledger và low-stock alert — 5–8 ngày công

1. **Mục tiêu:** đọc tồn sổ ước tính, mốc kiểm kê gần nhất, available và lịch sử đáng tin cậy.
2. **Dependency/Ready:** P03-S01 và recipes.
3. **Thứ tự:** aggregate selectors → availability calculation → ledger UI → alert/cache.
4. **DB `P03-S02-DB01`:** index movement/lot/ingredient/time; không lưu aggregate nếu chưa cần.
5. **BE `P03-S02-BE01..03`:** estimated-on-hand/available/expiring selectors, physical-count baseline,
   low-stock rules và query tests; không gắn nhãn tồn ước tính là tồn kiểm kê.
6. **FE `P03-S02-FE01..03`:** stock table/detail ledger, hiển thị nguồn và thời điểm kiểm kê gần nhất,
   filters, low/expiry badges and empty states.
7. **API `P03-S02-API01`:** `/inventory/stock/`, `/movements/`, `/alerts/` read-only scoped.
8. **Excel `P03-S02-XL01`:** export stock/ledger basic; full report refined Phase 8/10.
9. **Happy/error:** no movement, expired lot, negative invariant detection, large pagination.
10. **Acceptance:** totals reconcile movement; estimated/physical/available formula documented/tested.
11. **DoD:** selector/query/permission tests; UI filters/export match.
12. **Demo/evidence:** receipt changes stock; low/expiry indicator and ledger drill-down.
13. **Rủi ro/out:** chưa reservation/consumption/count.
14. **Effort:** 5–8 ngày.

### P03-S03 — Receipt Excel import và stock export — 4–7 ngày công

1. **Mục tiêu:** nhập dòng phiếu thành draft, xuất tồn theo filter.
2. **Dependency/Ready:** P02-S04, P03-S01/S02.
3. **Thứ tự:** receipt adapter/template → preview UI → draft confirm → export reconciliation.
4. **DB `P03-S03-DB01`:** reuse ImportJob; link created draft document.
5. **BE `P03-S03-BE01..03`:** reference/decimal/date validation, create draft only, export typed cells.
6. **FE `P03-S03-FE01..02`:** module wizard, navigate to created draft, export action/filter summary.
7. **API `P03-S03-API01`:** reuse imports; stock export endpoint.
8. **Excel `P03-S03-XL01..02`:** receipt line template/error file; stock workbook metadata.
9. **Happy/error:** duplicate line/ref, unknown code, stale price, confirm twice, no stock side effect.
10. **Acceptance:** import không post/approve; export full filtered result.
11. **DoD:** XLSX/security/transaction/E2E test pass.
12. **Demo/evidence:** import receipt draft, review/post separately, export stock.
13. **Rủi ro/out:** no partial import/background processing.
14. **Effort:** 4–7 ngày.

---

## Phase 4 — Bàn, ca tối thiểu và tạo đơn

### P04-S01 — Area/table và open shift — 5–8 ngày công

1. **Mục tiêu:** nền location và ca mở cho POS.
2. **Dependency/Ready:** Phase 3, role/permission ready.
3. **Thứ tự:** area/table CRUD → shift schema/open → employee UI/current shift state.
4. **DB `P04-S01-DB01..02`:** Area, CafeTable/status; Shift/opening cash/unique open constraint.
5. **BE `P04-S01-BE01..03`:** CRUD, open shift service/lock, current shift selector/permissions.
6. **FE `P04-S01-FE01..03`:** table map/list, open-shift dialog, current-shift shell/banner.
7. **API `P04-S01-API01`:** `/areas/`, `/tables/`, `/shifts/current/`, `/shifts/open/`.
8. **Excel:** không áp dụng.
9. **Happy/error:** duplicate table code, disabled table, second open shift, invalid opening cash.
10. **Acceptance:** POS action cần ca bị chặn rõ; customer ordering không cần employee shift.
11. **DoD:** unique/concurrency/permission tests + responsive UI.
12. **Demo/evidence:** admin tạo bàn, employee mở ca và refresh vẫn nhận current shift.
13. **Rủi ro/out:** close/reconciliation Phase 7.
14. **Effort:** 5–8 ngày.

### P04-S02 — Cart, POS và customer order creation — 9–13 ngày công

1. **Mục tiêu:** tạo order draft/pending từ customer hoặc POS với total server-side.
2. **Dependency/Ready:** P02 menu, P04-S01; snapshot/customization contract khóa.
3. **Thứ tự:** order schema/service → customer cart/checkout → POS → detail/history.
4. **DB `P04-S02-DB01..03`:** Order, Line, LineOption, StatusEvent, snapshot/money constraints/indexes.
5. **BE `P04-S02-BE01..04`:** create/reprice/validate, customer ownership, POS source/shift/table rules.
6. **FE `P04-S02-FE01..05`:** Pinia cart, cart drawer/page, checkout, POS product grid/cart, order detail.
7. **API `P04-S02-API01`:** `POST /orders/`, list/detail scoped; client không gửi trusted total.
8. **Excel:** order import cấm; export ở Phase 10.
9. **Happy/error:** price changed, option unavailable, table occupied, empty cart, duplicate submit/retry.
10. **Acceptance:** order total/snapshot đúng; customer chỉ thấy own orders; POS gắn actor/shift.
11. **DoD:** idempotency/ownership/total tests + customer/POS E2E API thật.
12. **Demo/evidence:** customer và POS tạo hai loại order, refresh detail/history.
13. **Rủi ro/out:** chưa accept/pay/prepare; order không tự giữ stock.
14. **Effort:** 9–13 ngày.

### P04-S03 — Accept, reserve, cancel và expiry — 9–13 ngày công

1. **Mục tiêu:** xác nhận khả năng phục vụ và giữ kho an toàn.
2. **Dependency/Ready:** P03 stock/recipe, P04-S02 order.
3. **Thứ tự:** reservation schema/service → accept action → cancel/release → expiry command/UI.
4. **DB `P04-S03-DB01..02`:** StockReservation/Line/status/expiry/unique order; supporting indexes.
5. **BE `P04-S03-BE01..05`:** recipe expansion, atomic availability lock/reserve, cancel policy/release,
   expiration management command, concurrency tests.
6. **FE `P04-S03-FE01..04`:** employee accept/reject, customer cancel, countdown/status timeline, conflicts.
7. **API `P04-S03-API01`:** `/orders/{id}/confirm|reject|cancel/`; 409 insufficient/stale.
8. **Excel:** không áp dụng.
9. **Happy/error:** two competing orders, recipe missing, already paid, already preparing, retry action.
10. **Acceptance:** không oversell; cancel/expire release đúng một lần; paid/preparing không cancel.
11. **DoD:** transaction/race/idempotency/ownership tests + E2E accept/cancel.
12. **Demo/evidence:** cạnh tranh stock, một order conflict; cancel trả available.
13. **Rủi ro/out:** scheduler production cho expiry thiết kế deployment Phase 11; không refund.
14. **Effort:** 9–13 ngày.

---

## Phase 5 — Thanh toán, pha chế và hoàn thành

### P05-S01 — Cash và manual transfer payment — 7–11 ngày công

1. **Mục tiêu:** ghi nhận thanh toán đúng quyền, ca và idempotency; không refund.
2. **Dependency/Ready:** order confirmed/reserved, shift open; payment state decision khóa.
3. **Thứ tự:** payment schema → cash flow → transfer report/confirm → UI/history/test.
4. **DB `P05-S01-DB01..02`:** PaymentAttempt, PaymentEvent, idempotency/reference/amount constraints.
5. **BE `P05-S01-BE01..05`:** initiate/report/confirm/reject services, shift/permission/order-state guard,
   aggregate paid status, concurrency/idempotency tests.
6. **FE `P05-S01-FE01..04`:** customer payment instructions/report, cashier dialog, transfer queue,
   payment timeline/receipt state.
7. **API `P05-S01-API01`:** `/orders/{id}/payments/`, `/payments/{id}/report|confirm|reject/`.
8. **Excel:** không import payment/revenue; export Phase 10.
9. **Happy/error:** customer reports transfer, duplicate reference, wrong amount, closed shift, double confirm.
10. **Acceptance:** customer click không paid; only confirmed payment changes aggregate exactly once.
11. **DoD:** money/permission/race tests + cash/transfer E2E, OpenAPI.
12. **Demo/evidence:** cash confirm and transfer report→employee confirm; retry safe.
13. **Rủi ro/out:** không gateway/refund/split/overpayment nếu chưa mở scope.
14. **Effort:** 7–11 ngày.

### P05-S02 — Kitchen queue, start preparation và stock consumption — 9–13 ngày công

1. **Mục tiêu:** barista xử lý queue; bắt đầu pha trừ kho/lot đúng một lần.
2. **Dependency/Ready:** P05-S01 paid order; P04 reservation; lot/recipe available.
3. **Thứ tự:** line preparation state → queue selector/UI → start+consume transaction → ready state.
4. **DB `P05-S02-DB01..02`:** line status/timestamps/assignee; consumption allocation reference.
5. **BE `P05-S02-BE01..05`:** queue, claim/start, reservation→FEFO movement, mark ready, race/retry tests.
6. **FE `P05-S02-FE01..04`:** barista board, order/line card, elapsed status, start/ready actions/errors.
7. **API `P05-S02-API01`:** `/kitchen/orders/`, `/order-lines/{id}/start|ready/` or batched order action.
8. **Excel:** không áp dụng.
9. **Happy/error:** unpaid start, reservation expired/missing, insufficient lot due correction, two baristas.
10. **Acceptance:** movement/COGS allocation đúng; retry không trừ hai lần; không auto-return brewed stock.
11. **DoD:** transaction/FEFO/idempotency/permission tests + barista E2E.
12. **Demo/evidence:** paid order vào queue, start làm giảm on-hand và ready.
13. **Rủi ro/out:** không realtime websocket mặc định; polling bounded v1 nếu đủ.
14. **Effort:** 9–13 ngày.

### P05-S03 — Serve, complete, receipt và end-to-end order — 5–8 ngày công

1. **Mục tiêu:** hoàn tất dine-in/takeaway và lịch sử khách/nhân viên.
2. **Dependency/Ready:** P05-S02.
3. **Thứ tự:** serve/complete rules → employee/customer UI → printable receipt → E2E full flow.
4. **DB `P05-S03-DB01`:** completion/served timestamps và event metadata nếu chưa có.
5. **BE `P05-S03-BE01..03`:** serve/complete transition, table release, receipt selector.
6. **FE `P05-S03-FE01..04`:** pickup/serve actions, customer tracking/history, receipt view/print CSS.
7. **API `P05-S03-API01`:** `/orders/{id}/serve|complete/`, receipt/detail read model.
8. **Excel:** không áp dụng.
9. **Happy/error:** takeaway direct complete, dine-in requires served, incomplete lines, repeated action.
10. **Acceptance:** order terminal state đúng; table released; immutable history/payment/stock visible.
11. **DoD:** three-role E2E menu→order→pay→prepare→complete pass.
12. **Demo/evidence:** full cash and transfer scenarios, no mock.
13. **Rủi ro/out:** không cancel/refund sau paid.
14. **Effort:** 5–8 ngày.

---

## Phase 6 — Đánh giá khách hàng

### P06-S01 — Review, aggregate và moderation — 6–9 ngày công

1. **Mục tiêu:** review xác thực từ completed order và moderation không sửa lời khách.
2. **Dependency/Ready:** Phase 5 completed orders; edit-window decision.
3. **Thứ tự:** review schema/policy → customer create/edit → aggregates → admin moderation.
4. **DB `P06-S01-DB01..02`:** Review unique order-line/customer, moderation event/reason/index.
5. **BE `P06-S01-BE01..04`:** eligibility/ownership, create/update window, aggregate selector, hide/unhide.
6. **FE `P06-S01-FE01..04`:** eligible review form, purchase history CTA, product reviews, moderation table.
7. **API `P06-S01-API01`:** review CRUD limited, product aggregate/list, moderation actions.
8. **Excel:** review export deferred Phase 10; no review import.
9. **Happy/error:** non-purchased/incomplete/duplicate/expired edit, hidden review, admin edit attempt.
10. **Acceptance:** 1–5 only; one review/line; admin cannot change rating/content; reason audited.
11. **DoD:** eligibility/ownership/aggregate/permission tests + customer/admin E2E.
12. **Demo/evidence:** completed order review, aggregate change, admin hide with reason.
13. **Rủi ro/out:** no sentiment/AI moderation.
14. **Effort:** 6–9 ngày.

---

## Phase 7 — Thu chi và đối soát ca

### P07-S01 — Finance voucher và cash/bank ledger — 8–12 ngày công

1. **Mục tiêu:** thu/chi thủ công và liên kết receipt mà không ghi trùng sales.
2. **Dependency/Ready:** payment/receipt/permission stable; finance category decision.
3. **Thứ tự:** category/voucher/ledger schema → draft/approval/post → links → admin/employee UI.
4. **DB `P07-S01-DB01..03`:** FinanceCategory, Voucher/Line/Event, CashBankMovement immutable refs.
5. **BE `P07-S01-BE01..05`:** CRUD draft, approve/post lock, source uniqueness, receipt link, permissions.
6. **FE `P07-S01-FE01..04`:** voucher list/form/detail, approval queue, source links/ledger.
7. **API `P07-S01-API01`:** voucher CRUD/action, ledger read; source/type filters.
8. **Excel:** adapter ở P07-S03.
9. **Happy/error:** duplicate sales movement, negative/zero amount, posted edit, closed shift, permission.
10. **Acceptance:** sale cash movement exactly once; receipt expense linked, no complex supplier debt.
11. **DoD:** ledger reconciliation/idempotency/approval tests + UI/API.
12. **Demo/evidence:** manual expense draft→post và linked receipt expense.
13. **Rủi ro/out:** không accounting double-entry/payable aging/tax engine.
14. **Effort:** 8–12 ngày.

### P07-S02 — Close shift, cash count và reconciliation — 7–10 ngày công

1. **Mục tiêu:** đóng ca với expected/actual/difference và bàn giao.
2. **Dependency/Ready:** P07-S01, cash payments, open shift.
3. **Thứ tự:** close snapshot schema → expected calculation → count UI → close lock/report.
4. **DB `P07-S02-DB01`:** ShiftClosingCount/handover fields/events; closed snapshot immutable.
5. **BE `P07-S02-BE01..04`:** expected cash selector, closing service/lock, variance/reopen prohibition.
6. **FE `P07-S02-FE01..03`:** close wizard, denomination/actual input, variance confirm and summary.
7. **API `P07-S02-API01`:** `/shifts/{id}/closing-preview|close/`, detail/reconciliation.
8. **Excel:** shift summary export basic.
9. **Happy/error:** concurrent payment during close, already closed, mismatch acknowledgement, wrong actor.
10. **Acceptance:** snapshot reconciles opening + movements; no payment attaches after close.
11. **DoD:** concurrency/math/permission/E2E shift pass.
12. **Demo/evidence:** open→sales/expense→close with expected/actual/difference.
13. **Rủi ro/out:** no payroll/employee attendance.
14. **Effort:** 7–10 ngày.

### P07-S03 — Finance import/export — 4–7 ngày công

1. **Mục tiêu:** import voucher draft và export cash/bank ledger theo quyền.
2. **Dependency/Ready:** P02-S04, P07-S01/S02.
3. **Thứ tự:** template/adapter → preview/confirm draft → export/filter/reconcile.
4. **DB `P07-S03-DB01`:** reuse import link to created voucher batch.
5. **BE `P07-S03-BE01..03`:** category/reference/date/amount validation; draft-only; secure export.
6. **FE `P07-S03-FE01..02`:** finance import wizard/history and export action.
7. **API `P07-S03-API01`:** reuse imports + finance export.
8. **Excel `P07-S03-XL01..02`:** typed money/date, filter metadata, formula defense.
9. **Happy/error:** duplicate external ref, unknown category, invalid date, confirm twice, permission scope.
10. **Acceptance:** import không post/cash effect; export không trùng sales/manual movement.
11. **DoD:** transaction/XLSX/E2E tests.
12. **Demo/evidence:** import 2 draft expenses, approve separately, export filtered ledger.
13. **Rủi ro/out:** no bank statement auto-reconciliation.
14. **Effort:** 4–7 ngày.

---

## Phase 8 — Kiểm kê, hao hụt và giá vốn

### P08-S01 — Stock count, adjustment và wastage — 8–12 ngày công

1. **Mục tiêu:** điều chỉnh tồn bằng chứng từ duyệt, không sửa stock trực tiếp.
2. **Dependency/Ready:** Phase 3 ledger/lots, permissions, recipe consumption.
3. **Thứ tự:** count/wastage schema → draft capture → approve/post → ledger/UI.
4. **DB `P08-S01-DB01..03`:** StockCount/Line, Wastage/Line, reason/event, movement source constraints.
5. **BE `P08-S01-BE01..05`:** snapshot, variance, approval/post lock, lot allocation, immutable history.
6. **FE `P08-S01-FE01..04`:** count wizard, scan/search line entry, variance review, wastage form/approval.
7. **API `P08-S01-API01`:** count/wastage CRUD/actions; stock snapshot token for stale detection.
8. **Excel:** adapter ở S03.
9. **Happy/error:** stale count, negative result, expired/damaged reasons, post twice, concurrent receipt.
10. **Acceptance:** adjustment/wastage movement reconcile; brewed item không auto-return.
11. **DoD:** concurrency/lot/permission/rollback tests + E2E.
12. **Demo/evidence:** count variance approve/post; wastage expired lot.
13. **Rủi ro/out:** no IoT/barcode hardware integration.
14. **Effort:** 8–12 ngày.

### P08-S02 — COGS and inventory reconciliation — 6–9 ngày công

1. **Mục tiêu:** đối chiếu standard consumption/standard COGS với kiểm kê, hao hụt và variance thực tế.
2. **Dependency/Ready:** P05 consumption, P08-S01, finance terminology.
3. **Thứ tự:** formula/data audit → selectors → detail/drilldown UI → reconciliation tests.
4. **DB `P08-S02-DB01`:** index/cost snapshot completion; no retroactive rewrite of posted costs.
5. **BE `P08-S02-BE01..03`:** standard COGS per order/product/period, variance allocation, stock
   reconciliation và anomaly flags; không gọi standard quantity là actual consumption.
6. **FE `P08-S02-FE01..03`:** standard COGS summary, variance, movement drilldown và
   mismatch/expiry/wastage reports.
7. **API `P08-S02-API01`:** read-only cost/reconciliation endpoints with date/timezone filters.
8. **Excel:** report contract for S03/P10.
9. **Happy/error:** missing historical cost, backdated receipt policy, voided doc, timezone boundary.
10. **Acceptance:** formula documented; totals trace to movements/lots/order lines.
11. **DoD:** golden-data reconciliation tests and permissions.
12. **Demo/evidence:** trace one order từ recipe→standard consumption→lot cost, sau đó đối chiếu một
    physical count/wastage thành variance.
13. **Rủi ro/out:** không gọi gross margin là net profit.
14. **Effort:** 6–9 ngày.

### P08-S03 — Inventory Excel count/import and reports — 4–7 ngày công

1. **Mục tiêu:** import count draft và export stock/wastage/COGS.
2. **Dependency/Ready:** P02-S04, P08-S01/S02.
3. **Thứ tự:** count template/snapshot → preview/draft → report workbooks.
4. **DB `P08-S03-DB01`:** import link/version to count snapshot.
5. **BE `P08-S03-BE01..03`:** stale snapshot revalidation, draft-only, typed report exports.
6. **FE `P08-S03-FE01..02`:** count import wizard and report export actions.
7. **API `P08-S03-API01`:** reuse imports; inventory report export.
8. **Excel `P08-S03-XL01..03`:** count/wastage/COGS workbooks with filters/time/unit.
9. **Happy/error:** unknown code, duplicate ingredient, stale stock, permission, formula injection.
10. **Acceptance:** import không adjust tồn; export reconciles on-screen totals/source.
11. **DoD:** XLSX/stale/transaction/E2E test.
12. **Demo/evidence:** import physical count draft then approve; export COGS.
13. **Rủi ro/out:** no partial import/background job.
14. **Effort:** 4–7 ngày.

### P08-S04 — Đề xuất nhập nguyên liệu — 5–8 ngày công

1. **Mục tiêu:** dùng doanh số, recipe, hao hụt/yield và tồn thực tế để đề xuất lượng cần nhập.
2. **Dependency/Ready:** P05 order history, P08-S01/S02 reconciliation; supplier lead time và quy cách mua.
3. **Thứ tự:** khóa công thức → demand window/forecast đơn giản → suggestion service → review UI → test.
4. **DB `P08-S04-DB01..02`:** ingredient replenishment policy (safety stock, loss/yield, lead time,
   purchase pack/minimum); optional suggestion snapshot/audit, không nhân bản raw order.
5. **BE `P08-S04-BE01..04`:** demand từ completed order × recipe version, loss/yield adjustment,
   subtract available/pending receipts, pack rounding và reason breakdown.
6. **FE `P08-S04-FE01..03`:** danh sách đề xuất, kỳ dự báo, breakdown công thức, cảnh báo thiếu dữ liệu và
   hành động tạo phiếu nhập DRAFT có xác nhận riêng.
7. **API `P08-S04-API01`:** read-only suggestion/preview; action tạo receipt DRAFT idempotent, không POST.
8. **Excel `P08-S04-XL01`:** export đề xuất cùng inputs/as-of time/reason; không import trực tiếp movement.
9. **Happy/error:** chưa kiểm kê, recipe đổi giữa kỳ, pending receipt, yield bằng 0, pack rounding,
   supplier thiếu lead time và dữ liệu bán thưa.
10. **Acceptance:** kết quả truy được về order/recipe/count/receipt; không tự thay tồn hoặc tự đặt hàng.
11. **DoD:** golden fixture/formula/permission tests, UI breakdown và E2E tạo receipt DRAFT.
12. **Demo/evidence:** dự báo 100 ly, tính nhu cầu gross, trừ tồn/pending và làm tròn số gói cần mua.
13. **Rủi ro/out:** chưa tối ưu đa nhà cung cấp/giá/khuyến mãi; không tuyên bố ML khi chỉ dùng rule.
14. **Effort:** 5–8 ngày.

---

## Phase 9 — Recommendation system

### P09-S01 — Event collection, popular và similar — 7–10 ngày công

1. **Mục tiêu:** recommendation hữu ích có fallback, không tuyên bố ML giả.
2. **Dependency/Ready:** catalog/orders/reviews; event privacy/retention duyệt.
3. **Thứ tự:** audit events đã thu → event schema/API → popular → content-similar → surfaces.
4. **DB `P09-S01-DB01..02`:** RecommendationEvent, strategy/config/impression/result metadata/index.
5. **BE `P09-S01-BE01..04`:** event ingest validation, popular window, similarity features, availability filter.
6. **FE `P09-S01-FE01..03`:** recommendation rail customer/POS, impression/click/add tracking, fallback state.
7. **API `P09-S01-API01`:** `/recommendations/`, `/recommendation-events/` bounded/idempotent.
8. **Excel:** no import; metrics export Phase 10.
9. **Happy/error:** anonymous/new customer, no data, unavailable item, duplicate event, tracking blocked.
10. **Acceptance:** chỉ món active/servable; fallback deterministic; reason/strategy traceable.
11. **DoD:** ranking/filter/event tests + UI integration; baseline metric definition.
12. **Demo/evidence:** new-user popular, product similar, unavailable exclusion.
13. **Rủi ro/out:** không LLM/ML service/A-B platform.
14. **Effort:** 7–10 ngày.

### P09-S02 — Personalized/co-purchase và evaluation — 7–11 ngày công

1. **Mục tiêu:** gợi ý theo history/review và mua kèm, đo được hiệu quả.
2. **Dependency/Ready:** P09-S01 đủ event; minimum data threshold được chốt.
3. **Thứ tự:** co-purchase aggregates → preference score → fallback blending → metrics/admin config.
4. **DB `P09-S02-DB01`:** optional aggregate snapshot/version; do not duplicate raw orders unnecessarily.
5. **BE `P09-S02-BE01..04`:** co-purchase, user profile score, cold-start fallback, metric selectors.
6. **FE `P09-S02-FE01..03`:** personalized rail, POS upsell, admin strategy/metric view.
7. **API `P09-S02-API01`:** context-aware recommendation and metrics, permission scoped.
8. **Excel:** metric export Phase 10.
9. **Happy/error:** sparse history, negative/hidden review, sold-out related item, strategy failure.
10. **Acceptance:** fallback always safe; impression/click/add/purchase funnel calculable.
11. **DoD:** offline fixture evaluation and end-to-end tracking; không dùng fake data để claim impact.
12. **Demo/evidence:** known customer vs cold start, co-purchase in POS, metric funnel.
13. **Rủi ro/out:** ML chỉ mở khi đủ volume và có holdout/evaluation plan.
14. **Effort:** 7–11 ngày.

---

## Phase 10 — Dashboard và Excel báo cáo

### P10-S01 — Operational dashboards — 8–12 ngày công

1. **Mục tiêu:** dashboard đúng định nghĩa, drill-down tới nguồn.
2. **Dependency/Ready:** Phases 5–9 data stable; metric glossary duyệt.
3. **Thứ tự:** metric definitions → selectors/query budget → APIs → admin/employee dashboard.
4. **DB `P10-S01-DB01`:** index by time/status/source; materialized aggregate chỉ khi profiling yêu cầu.
5. **BE `P10-S01-BE01..04`:** revenue/order/product, cash/expense, stock/COGS/wastage, review/reco metrics.
6. **FE `P10-S01-FE01..04`:** filter/date presets, stat cards/charts/tables, drilldown, loading/empty/error.
7. **API `P10-S01-API01`:** `/reports/*` read-only, timezone/filter/scope contract.
8. **Excel:** workbook ở S02.
9. **Happy/error:** no data, partial current day, timezone cutoff, hidden review, late posted voucher.
10. **Acceptance:** revenue ≠ receipt ≠ cash balance ≠ COGS; no false net-profit label.
11. **DoD:** golden fixture formula/query/permission tests; responsive chart + accessible table.
12. **Demo/evidence:** date filter and drill-down reconciles exact transaction rows.
13. **Rủi ro/out:** không data warehouse/real-time BI.
14. **Effort:** 8–12 ngày.

### P10-S02 — Report workbooks và export center — 7–10 ngày công

1. **Mục tiêu:** xuất doanh thu/chi phí/dòng tiền/đơn/tồn/COGS/review/reco đúng filter.
2. **Dependency/Ready:** P10-S01 definitions; export limits/retention.
3. **Thứ tự:** workbook specs → exporters → export center UI → reconcile/security/performance.
4. **DB `P10-S02-DB01`:** ExportJob metadata only if history required; sync v1 within limit.
5. **BE `P10-S02-BE01..04`:** module exporters, full-filter query, typed cells/totals, audit/permission.
6. **FE `P10-S02-FE01..03`:** export drawer/center, filter summary, progress/result/error/history.
7. **API `P10-S02-API01`:** `/exports/` create/download/history or direct bounded download.
8. **Excel `P10-S02-XL01..05`:** revenue, finance, orders, inventory/COGS, review/reco reports.
9. **Happy/error:** 0 rows, row limit, permission-scoped fields, formula injection, timeout.
10. **Acceptance:** toàn bộ filtered result, metadata/timezone/unit, totals reconcile dashboard.
11. **DoD:** golden workbook/security/limit/E2E tests.
12. **Demo/evidence:** export each family and reconcile sample totals.
13. **Rủi ro/out:** background queue only if measured export exceeds sync budget.
14. **Effort:** 7–10 ngày.

---

## Phase 11 — Kiểm thử tổng thể và bàn giao

### P11-S01 — Critical E2E, security và concurrency — 7–11 ngày công

1. **Mục tiêu:** chứng minh luồng ba role và invariant tiền/kho/import.
2. **Dependency/Ready:** tất cả feature scope freeze; seeded deterministic dataset.
3. **Thứ tự:** risk matrix → integration/concurrency tests → E2E roles → fix regressions.
4. **DB `P11-S01-DB01`:** migration plan rehearsal; constraint/index audit; backup before destructive drill.
5. **BE `P11-S01-BE01..04`:** ownership/permission, payment/reservation/consumption race, posting/import retry.
6. **FE `P11-S01-FE01..03`:** customer/employee/admin E2E, stale/offline/error handling, no mocks.
7. **API `P11-S01-API01`:** OpenAPI diff/compatibility/status/error audit.
8. **Excel `P11-S01-XL01`:** end-to-end invalid/stale/double-confirm/export permission suite.
9. **Happy/error:** full lifecycle plus 401/403/409/429/network/5xx and retry.
10. **Acceptance:** critical suite repeatable; no duplicate money/stock; access violations blocked.
11. **DoD:** CI green; defects critical/high closed or explicitly accepted.
12. **Demo/evidence:** automated report + trace IDs/ledger reconciliation.
13. **Rủi ro/out:** penetration test chuyên nghiệp ngoài scope nhưng checklist security phải xong.
14. **Effort:** 7–11 ngày.

### P11-S02 — Responsive, accessibility, motion và performance — 5–8 ngày công

1. **Mục tiêu:** UX usable trên target sizes và 3D/motion không gây regression.
2. **Dependency/Ready:** P11-S01 feature-stable.
3. **Thứ tự:** accessibility audit → responsive/device → performance profile → fixes.
4. **DB:** không đổi trừ index có bằng chứng profiling.
5. **BE `P11-S02-BE01`:** query count/slow endpoint/bundle response profiling.
6. **FE `P11-S02-FE01..04`:** keyboard/screen reader/contrast, breakpoints/zoom, reduced motion/3D cleanup,
   route/bundle/image/table performance.
7. **API:** payload/pagination/cache review; không đổi contract không cần thiết.
8. **Excel:** large-within-limit UX/time/memory smoke.
9. **Happy/error:** slow network/device, WebGL fail, font/image fail, long labels/data.
10. **Acceptance:** WCAG AA mục tiêu critical flow; no blocking animation; agreed budgets met.
11. **DoD:** audit evidence 375/768/1024/1440, zoom 200%, reduced motion, Lighthouse/profile.
12. **Demo/evidence:** report before/after và device screenshots/video.
13. **Rủi ro/out:** formal WCAG certification và all-device lab ngoài scope.
14. **Effort:** 5–8 ngày.

### P11-S03 — Deployment, backup/restore và handoff — 6–9 ngày công

1. **Mục tiêu:** vận hành được, rollback/backup rõ và tài liệu bàn giao hoàn chỉnh.
2. **Dependency/Ready:** P11-S01/S02 green; target hosting được chọn.
3. **Thứ tự:** production config → migration/release → backup/restore drill → monitoring/runbook/demo.
4. **DB `P11-S03-DB01..03`:** backup/restore, migration forward-fix rehearsal, retention/maintenance.
5. **BE `P11-S03-BE01..03`:** secure env, Gunicorn/reverse proxy/static/health/log/scheduled commands.
6. **FE `P11-S03-FE01..02`:** production build/base URL/error monitoring hooks/deploy checks.
7. **API `P11-S03-API01`:** HTTPS/CORS/CSRF/host/proxy/rate-limit production verification.
8. **Excel `P11-S03-XL01`:** artifact storage/retention/permission/cleanup runbook.
9. **Happy/error:** failed migration, DB/Redis unavailable, restore, disk/file cleanup, rollback decision.
10. **Acceptance:** fresh deploy + restore + smoke works from documented steps.
11. **DoD:** README/runbook/demo seed/known issues/release checklist signed off.
12. **Demo/evidence:** deployment rehearsal, backup checksum/restore query, three-role demo script.
13. **Rủi ro/out:** provider-specific HA/autoscale/SLA chỉ khi hosting scope có.
14. **Effort:** 6–9 ngày.

---

## Bảng tổng hợp Phase/Sprint

| Phase | Sprint                 | Deliverable chạy được                     | Effort |
| ----- | ---------------------- | ----------------------------------------- | -----: |
| 0     | S01 Audit/plan         | Bộ tài liệu + bằng chứng gate             |   2–3d |
| 0     | S02 Normalization      | Local/CI formatter/tooling xanh           |   2–4d |
| 0     | S03 Domain contracts   | Schema/state/quyền/idempotency được duyệt |   3–5d |
| 1     | S01 Components         | Token + custom components + showcase      |   6–9d |
| 1     | S02 Auth/layout        | Registration + 3 role + permission/layout |  7–10d |
| 1     | S03 Landing motion     | Customer home + lazy 3D/GSAP fallback     |   4–7d |
| 2     | S01 Catalog admin      | Catalog/variant/topping/price CRUD        |  7–10d |
| 2     | S02 Customer menu      | Menu/search/filter/customization          |   5–8d |
| 2     | S03 Inventory master   | Ingredient/unit/supplier/recipe           |  8–12d |
| 2     | S04 Excel master       | Template/preview/confirm/history/export   |  8–12d |
| 3     | S01 Receipt/lot        | Draft→approve→post nhập kho               |  8–12d |
| 3     | S02 Stock ledger       | On-hand/available/alerts/history          |   5–8d |
| 3     | S03 Stock Excel        | Receipt draft import + stock export       |   4–7d |
| 4     | S01 Table/open shift   | Khu vực/bàn + ca mở                       |   5–8d |
| 4     | S02 Order creation     | Customer cart + POS order                 |  9–13d |
| 4     | S03 Reservation/cancel | Accept/reserve/cancel/expire an toàn      |  9–13d |
| 5     | S01 Payment            | Cash/manual transfer confirm              |  7–11d |
| 5     | S02 Kitchen/consume    | Queue + prepare + stock consumption       |  9–13d |
| 5     | S03 Complete           | Serve/complete/receipt/full E2E           |   5–8d |
| 6     | S01 Reviews            | Verified review + moderation              |   6–9d |
| 7     | S01 Finance            | Voucher + cash/bank ledger                |  8–12d |
| 7     | S02 Shift close        | Count/handover/reconciliation             |  7–10d |
| 7     | S03 Finance Excel      | Draft import + ledger export              |   4–7d |
| 8     | S01 Count/wastage      | Inventory count/adjust/wastage            |  8–12d |
| 8     | S02 COGS               | Cost/reconciliation/drilldown             |   6–9d |
| 8     | S03 Inventory Excel    | Count draft import + reports              |   4–7d |
| 9     | S01 Baseline recs      | Events + popular + similar + fallback     |  7–10d |
| 9     | S02 Personalized       | History/co-purchase + evaluation          |  7–11d |
| 10    | S01 Dashboards         | Operational metrics + drilldown           |  8–12d |
| 10    | S02 Report Excel       | Export center + report workbooks          |  7–10d |
| 11    | S01 Critical QA        | 3-role E2E/security/concurrency           |  7–11d |
| 11    | S02 UX/performance     | A11y/responsive/motion/performance        |   5–8d |
| 11    | S03 Handoff            | Deploy/backup/restore/runbook             |   6–9d |

Tổng sơ bộ: **203–310 ngày công** cho một full-stack developer nếu làm toàn bộ scope và quality gate.
Khoảng này cần được re-estimate sau P00-S03 và mỗi phase; không chuyển thành lịch cam kết khi chưa biết
capacity, feedback latency, asset và hosting.

## Sprint nên bắt đầu đầu tiên

Sau khi người dùng duyệt kế hoạch, bắt đầu **P00-S02 — Tooling và base normalization**. Không bắt đầu
catalog hay UI mới khi formatter/toolchain còn đỏ và working-tree change chưa được phân loại. Sau P00-S02,
chạy P00-S03 để duyệt quyết định schema; rồi mới vào Phase 1.
