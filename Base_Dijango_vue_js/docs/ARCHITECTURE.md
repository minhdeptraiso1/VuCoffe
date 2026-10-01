# Kiến trúc mục tiêu

## Topology

Giữ monorepo hai ứng dụng và backend modular monolith. Vue gọi REST `/api/v1/`; Django/PostgreSQL là nguồn
sự thật. Redis phục vụ cache, throttle và lock ngắn hạn có thể tái tạo. Không thêm microservice/Celery cho
MVP nếu chưa có bằng chứng tải.

## Backend modules dự kiến

| App               | Trách nhiệm                                                                           |
| ----------------- | ------------------------------------------------------------------------------------- |
| `accounts`        | User, auth, registration, coarse role, permission output                              |
| `catalog`         | Category, product, variant, topping, option, price/availability                       |
| `inventory`       | Unit, ingredient, supplier, recipe, receipt, lot, ledger, reservation, count, wastage |
| `locations`       | Area, table                                                                           |
| `orders`          | Cart/order/line/customization, state transition, kitchen queue                        |
| `payments`        | Cash/manual transfer attempt và payment history                                       |
| `shifts`          | Open/close shift, cash count, handover                                                |
| `finance`         | Income/expense category, voucher, cash/bank ledger, receipt link                      |
| `reviews`         | Rating/content/moderation                                                             |
| `recommendations` | Strategy/config/result/event; v1 chạy trong monolith                                  |
| `imports`         | Template, upload, preview, confirm, row issue, artifact/history                       |
| `reports`         | Read-only aggregate/export orchestration; không sở hữu transaction nguồn              |

App dùng model/service/selector/api như chuẩn hiện tại. Cross-module write đi qua public service rõ ràng;
không dùng signal cho luồng payment/stock/order chính.

## Identity và permission

- Ba coarse role: `ADMIN`, `EMPLOYEE`, `CUSTOMER`.
- Dùng ba reserved Django Group `role:admin`, `role:employee`, `role:customer`; service bảo đảm mỗi user
  thuộc đúng một reserved role group. Các group `duty:*` không phải role và có thể gán thêm cho employee.
- ADMIN có toàn quyền theo policy; EMPLOYEE nhận granular `auth.Permission` qua duty group như cashier,
  barista hoặc inventory; CUSTOMER dựa vào ownership và action allowlist.
- `/auth/me/` trả role và permission codes cần cho UI; không trả permission vượt nhu cầu.
- Admin dùng `GET/POST /auth/employees/` để đọc danh sách có pagination/tạo employee,
  `GET /auth/permissions/` để lấy catalog quyền có thể cấp và
  `PATCH /auth/employees/{id}/permissions/` để thay toàn bộ granular permissions.
- Catalog và input cấp quyền loại permission của các app hạ tầng (`auth`, `admin`, `contenttypes`,
  `sessions`, `token_blacklist`); coarse role vẫn là lớp bảo vệ độc lập.
- Permission được đọc lại từ database ở request kế tiếp nên revoke có hiệu lực mà không chờ access token
  hết hạn; user inactive bị authentication backend từ chối ngay.
- Query selector luôn scope theo actor; action service kiểm tra permission + ownership + state.
- Không cài object-permission package khi policy đơn giản có thể diễn đạt/test trực tiếp.

## Mô hình dữ liệu cốt lõi

### Catalog

`Category 1—N Product 1—N ProductVariant`; `Topping` liên kết variant qua allowlist; giá hiện hành có
effective time hoặc price history. Product/variant dùng stable code, `is_active`, availability window.
Order line lưu snapshot code/name/size/unit price/customization.

### Inventory

`Unit`, `Ingredient(base_unit, precision, reorder_level, lot_tracking)`, `UnitConversion`, `Supplier`,
`RecipeItem(sellable_ref, ingredient, qty_base)`. `StockReceipt`/line tạo `InventoryLot` khi posted;
mọi thay đổi quantity đi qua append-only `StockMovement`.

`StockReservation`/line giữ lượng ước tính theo công thức. Inventory phải công khai hai khái niệm:

- `estimated_on_hand`: tồn sổ/ước tính, lấy chứng từ nhập/điều chỉnh đã POSTED trừ tiêu hao chuẩn theo
  order và reservation đang hoạt động; dùng để cảnh báo khả năng phục vụ và lập kế hoạch ngắn hạn.
- `physical_count`: lượng thực đếm tại lần kiểm kê gần nhất; là mốc xác nhận thực tế, sau đó tiếp tục được
  chiếu theo các movement có chứng từ cho tới lần kiểm kê kế tiếp.

Khi bắt đầu pha, reservation được chuyển thành **standard consumption** theo recipe version snapshot và
phân bổ lot theo FEFO cho mục đích sổ kho/giá vốn chuẩn. Movement này không tuyên bố lượng vật lý đã dùng
chính xác tuyệt đối. Sai số cân đong, bay hơi, sơ chế, đổ bỏ và hư hỏng được ghi bằng wastage/count
adjustment có audit; Phase 8 đối chiếu standard consumption với physical count. Quantity dùng decimal base
unit. Unit cost lấy snapshot theo lot; giá vốn ban đầu là standard COGS và được báo cáo cùng variance, không
gọi là actual COGS khi chưa đối chiếu.

Đề xuất nhập dùng forecast bán × recipe × hệ số hao hụt/yield, cộng tồn an toàn rồi trừ tồn khả dụng và
hàng đang chờ nhận. Kết quả làm tròn theo quy cách mua và chỉ là gợi ý; chi tiết tại
`docs/INVENTORY_REPLENISHMENT.md`.

Precision chuẩn: money `DecimalField(max_digits=14, decimal_places=2)`, quantity base unit
`DecimalField(max_digits=18, decimal_places=6)`, conversion factor
`DecimalField(max_digits=18, decimal_places=8)`. API serialize decimal thành string; không dùng float.

### Order/payment

`Order`, `OrderLine`, `OrderLineOption`, `OrderStatusEvent`; source `CUSTOMER_WEB|POS`, fulfillment
`DINE_IN|TAKEAWAY`, table nullable. `PaymentAttempt` tách khỏi order và có method/status/reference/actor.
Order có total snapshot và aggregate payment status; không suy ra paid từ input client.

### Shift/finance

`Shift` gắn employee/opening cash/status; `CashMovement` là ledger tiền mặt. Payment cash tạo movement
đúng một lần. `FinanceVoucher` draft→approved→posted/void; supplier receipt expense link bằng reference,
không tạo công nợ phức tạp. Report đọc ledger nguồn, không nhập doanh thu thủ công.

### Review/recommendation

`Review` unique theo completed order line/customer; rating 1–5, content, edit deadline, moderation state/
reason. Customer được sửa trong 7 ngày sau completion; admin chỉ hide/unhide và ghi lý do.

`RecommendationEvent` ghi impression/click/add-to-order/purchase theo product, actor/session/context.
Không lưu token/PII không cần thiết. Strategy v1: popular + similar content + co-purchase fallback.

## State machines

### Order

`DRAFT → PENDING_CONFIRMATION → CONFIRMED → IN_PREPARATION → READY → SERVED → COMPLETED`

- `DRAFT/PENDING_CONFIRMATION → CANCELLED|EXPIRED` khi chưa paid/chưa pha; release reservation nếu có.
- Reservation tạo tại `CONFIRMED`; bắt đầu pha yêu cầu paid và chuyển reservation → standard consumption.
- `READY → COMPLETED` trực tiếp cho takeaway nếu giao tại quầy; dine-in đi qua `SERVED`.
- Không transition từ paid/in-preparation sang cancelled trong MVP.

### Payment attempt

- Cash: `INITIATED → CONFIRMED` bởi employee có quyền trong shift mở.
- Transfer: `INITIATED → CUSTOMER_REPORTED → CONFIRMED|REJECTED` bởi employee; customer report không paid.
- Retry dùng idempotency key; tổng confirmed không vượt total trong phạm vi không split/overpay.

### Receipt/count/wastage/voucher

`DRAFT → SUBMITTED → APPROVED → POSTED`; có thể `REJECTED` trước POSTED. Sau POSTED không edit/delete;
sửa sai bằng chứng từ điều chỉnh/void theo policy, không sửa movement cũ.

### Shift

`OPEN → CLOSING → CLOSED`; mỗi employee tối đa một shift OPEN, POS payment cash phải gắn shift mở. Close
snapshot expected/actual/difference và người bàn giao/nhận.

### Import

`UPLOADED → VALIDATED → READY_TO_CONFIRM → CONFIRMING → COMPLETED`; nhánh `INVALID|STALE|FAILED`.
Confirm chỉ một lần, revalidate DB version/reference trước write.

## Transaction và concurrency

- `select_for_update`/conditional update cho accept order, reservation, start preparation, payment confirm,
  document posting và shift close.
- Header `Idempotency-Key` bắt buộc cho create order, payment action, document posting và import confirm.
  Key được scope theo actor + operation, gắn vào entity/action record bằng unique constraint; cùng key và
  cùng payload trả lại kết quả trước, cùng key nhưng payload khác trả `409`.
- Tổng order và availability được tính lại server-side trong transaction; không tin total/preview FE.
- API trả `409 conflict` cho stale state/concurrency; response lỗi theo contract hiện tại.
- Không giữ DB transaction trong lúc parse file hoặc gọi tác vụ chậm; parse/validate trước, transaction chỉ
  cho confirm/write bounded.

## API conventions bổ sung

- List endpoint: `page`, allowlisted filters, `ordering`; export dùng cùng filter nhưng không chỉ current page.
- Action endpoint rõ: `/orders/{id}/confirm/`, `/payments/{id}/confirm/`, `/receipts/{id}/post/`.
- PATCH chỉ sửa draft/mutable fields; transition dùng action endpoint để audit/idempotency rõ.
- Decimal serialize string; datetime ISO 8601 timezone-aware; money VND vẫn lưu decimal chính xác.
- OpenAPI cập nhật cùng feature; error 400/401/403/404/409/429 được mô tả ở action quan trọng.

## Frontend architecture

Giữ `modules/<domain>/{api,types,schemas,stores,composables,components,pages}`. Server state không đẩy hết
vào Pinia: page/composable giữ fetch state; Pinia cho auth, cart, current shift và state dùng xuyên route.
Route lazy-load theo role/surface; Three.js/GSAP lazy-load riêng customer home. Shared UI không import
domain. API module dùng duy nhất `apiClient`.

## Audit và retention

Các entity transaction có `created_by`, `approved_by/posted_by`, timestamps, status events và reference.
Không hard-delete paid order, payment, posted stock/cash movement, closed shift hoặc import history. PII và
file import/export có retention/permission; secret/token không ghi log/file.
