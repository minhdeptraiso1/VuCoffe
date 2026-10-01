# Import/export Excel specification

Trạng thái: contract kế hoạch; triển khai nền ở Phase 2 và mở rộng theo từng module.

## Công nghệ và giới hạn v1

- Đề xuất backend dùng `openpyxl` sau khi dependency được duyệt/khóa trong `uv.lock`.
- Chỉ `.xlsx`; không chạy macro, external link hay công thức. Cell bắt đầu bằng `=`, `+`, `-`, `@` từ dữ
  liệu người dùng phải được escape khi export để ngăn formula injection.
- Mặc định tối đa 5 MB, 5.000 data row và 30 column/import; từng module có thể thấp hơn.
- Xử lý đồng bộ v1; trả lỗi rõ nếu vượt limit. Chỉ thiết kế background job khi đo được nhu cầu.
- File/artifact có access control và retention đề xuất 30 ngày; metadata/audit giữ lâu hơn theo policy.

## Module và semantics

| Module                           | Import | Chế độ          | Kết quả confirm                  |
| -------------------------------- | ------ | --------------- | -------------------------------- |
| Category/product/variant/topping | Có     | create/update   | Ghi catalog                      |
| Ingredient/unit/conversion       | Có     | create/update   | Ghi master data, không đổi tồn   |
| Supplier                         | Có     | create/update   | Ghi master data                  |
| Receipt lines                    | Có     | create document | Tạo phiếu nhập DRAFT             |
| Stock count lines                | Có     | create document | Tạo phiếu kiểm kê DRAFT          |
| Manual income/expense            | Có     | create document | Tạo voucher DRAFT                |
| Revenue/order/payment            | Không  | export only     | Không cho ghi đè nguồn giao dịch |
| Reports/stock ledger             | Không  | export only     | File thống kê                    |

## Stable keys và ô trống

- Template dùng `code` ổn định; tên hiển thị không là khóa duy nhất.
- Create: ô bắt buộc trống là lỗi; optional trống dùng default/null theo data dictionary.
- Update: mặc định ô trống nghĩa là giữ nguyên. Muốn xóa nullable value dùng sentinel `__CLEAR__`, được
  khai báo trong template; field không nullable từ chối sentinel.
- Code trùng trong file là lỗi. Update code không tồn tại là lỗi trừ mode `upsert` được module cho phép.
- Quan hệ tham chiếu bằng stable code; validate active/status phù hợp.

## Workbook contract

- Sheet `Instructions`: version template, module, mode, generated_at, quy tắc và ví dụ; không import.
- Sheet `Data`: header cố định, machine key ở row kỹ thuật hoặc mapping được ký/version hóa.
- Sheet `Reference` tùy chọn: enum/code hợp lệ tại thời điểm tải; chỉ hỗ trợ người dùng, server vẫn kiểm tra.
- Template có `template_version`; server từ chối version không còn hỗ trợ với hướng dẫn tải bản mới.

## Workflow API

1. `GET /api/v1/imports/templates/{module}/` tải template theo quyền.
2. `POST /api/v1/imports/` multipart gồm module/mode/file, tạo job và validate.
3. `GET /api/v1/imports/{id}/` trả summary, preview có pagination và row issues.
4. `GET /api/v1/imports/{id}/error-file/` tải annotated/error workbook nếu có.
5. `POST /api/v1/imports/{id}/confirm/` cùng idempotency key; server revalidate và write.
6. `GET /api/v1/imports/` xem history trong phạm vi quyền.

FE không gửi dữ liệu preview làm nguồn ghi. Confirm chỉ gửi job ID/idempotency key. Server dùng file hash,
template version, actor, mode, validated-at và dependency/version fingerprints để phát hiện stale data.

## Validation

- File signature/extension/size/sheet/header/template version.
- Required, type, max length, decimal scale, non-negative, date/timezone, enum và stable code.
- Duplicate trong file/database, foreign reference, permission và mutable state.
- Tiền/quantity không dùng float; unit conversion không tạo cycle/ambiguous path.
- Lỗi có row, column, field code, stable error code, message tiếng Việt và raw value đã sanitize.
- Mặc định một lỗi bất kỳ khiến job INVALID và không ghi dòng nào.

## Confirm và transaction

- Lock job; state phải `READY_TO_CONFIRM`, actor còn quyền, chưa confirm trước đó.
- Re-run validation phụ thuộc DB; nếu khác preview thì state `STALE`, yêu cầu validate/tải lại.
- Master-data import ghi trong transaction bounded. Document import chỉ tạo DRAFT; posting/approval là
  workflow riêng và không nằm trong confirm import.
- Lưu counts new/update/error/skipped, actor/timestamp, hash, module, mode, result và error summary.

## Export

- Endpoint export dùng cùng filter/sort/scope với list nhưng bỏ pagination; không xuất ngoài quyền.
- Metadata đầu file: report name, generated_at/timezone, actor, filters, unit/currency.
- Ngày và số là cell type thật; tiền có number format; tổng chỉ thêm khi công thức nghiệp vụ rõ.
- Dữ liệu lớn có row limit và thông báo; không âm thầm xuất current page.
- Không xuất password hash, token, secret, refresh cookie, internal permission không cần thiết hoặc PII vượt quyền.

## Test bắt buộc

- Template/version đúng và sai; duplicate code; missing reference; decimal/date/enum; file quá limit.
- Blank-vs-clear update; create/update summary; file lỗi row/column.
- Confirm lặp/idempotency; stale data giữa preview-confirm; permission bị thu hồi.
- Transaction rollback toàn bộ khi một write lỗi.
- Receipt/count/voucher chỉ tạo DRAFT, không đổi stock/cash.
- Formula injection export; filter full result; unauthorized column/row không xuất.
