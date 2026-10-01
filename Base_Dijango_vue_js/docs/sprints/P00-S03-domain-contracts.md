# P00-S03 — Contract nền domain, quyền và concurrency

Status: Done

## Mục tiêu và dependency

Khóa các quyết định ảnh hưởng schema/API trước Phase 1–3. Dependency P00-S02 đã đạt; không tạo model,
migration hoặc API nghiệp vụ trong sprint này.

## Task checklist

- [x] P00-S03-DB01 — Khóa role groups, money/quantity/conversion precision và ledger immutability.
- [x] P00-S03-BE01 — Khóa permission/ownership, state transition, lock và idempotency convention.
- [x] P00-S03-FE01 — Khóa role/permission output, 403/409 và stale-state UX contract.
- [x] P00-S03-API01 — Khóa action endpoint, decimal string và `Idempotency-Key` semantics.
- [x] P00-S03-XL01 — Khóa XLSX 5 MB/5.000 dòng, blank/`__CLEAR__`, preview/confirm.
- [x] P00-S03-DOC01 — Chuyển product decisions từ Proposed sang Accepted.
- [x] P00-S03-QA01 — Kiểm tra consistency giữa scope/architecture/Excel/roadmap.

## Contract đã khóa

- Một reserved role group/user; employee có thể nhận nhiều `duty:*` groups.
- Money 14,2; quantity 18,6; conversion 18,8; decimal API là string.
- Order/payment tách state; reserve khi confirm, consume khi bắt đầu pha.
- Stock/cash ledger append-only; posted data không hard-delete.
- `Idempotency-Key` scope actor + operation; key trùng payload khác trả 409.
- Review unique per completed order line và sửa tối đa 7 ngày.
- Import sync 5 MB/5.000 dòng, document import chỉ tạo DRAFT.
- Recommendation v1 rule/content/co-purchase; Three.js chỉ customer hero; không dark mode trong MVP.

## Acceptance criteria / DoD

- Không còn decision `Proposed` chặn schema Phase 1–3.
- Architecture mô tả đủ role, precision, state, ledger, lock và idempotency.
- Excel spec có limit, stable key, blank/clear, stale/double-confirm và security.
- Không có runtime/business-code change trong P00-S03.

## Verification evidence

| Kiểm tra                                                 | Kết quả |
| -------------------------------------------------------- | ------- |
| Cross-reference scope/architecture/decisions/import plan | Pass    |
| 33 sprint có dependency và task DB/BE/FE/API/QA          | Pass    |
| Prettier tài liệu Phase 0                                | Pass    |

## Risks và input tương lai

- Tên/logo chính thức chưa có; Phase 1 dùng text mark/fallback để không chặn.
- Ingredient cần lot tracking được cấu hình theo dữ liệu Phase 2/3; cơ chế FEFO đã khóa.
- Thay precision/state/idempotency sau khi có dữ liệu cần ADR và migration/compatibility plan.

## Demo script

Walkthrough role matrix, order/payment/reservation state, một retry payment bằng cùng idempotency key và
workflow Excel preview→stale check→confirm.
