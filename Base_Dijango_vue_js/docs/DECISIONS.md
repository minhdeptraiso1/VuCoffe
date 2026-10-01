# Product architecture decisions

Các ADR base trong `docs/standards/architecture-decisions.md` vẫn là nguồn hiện hành. Các quyết định dưới
đây đã được khóa trong Phase 0; thay đổi sau này phải có ADR/migration/compatibility plan tương ứng.

| ID       | Quyết định                                                           | Trạng thái        | Lý do/ảnh hưởng                                                         |
| -------- | -------------------------------------------------------------------- | ----------------- | ----------------------------------------------------------------------- |
| PROD-001 | Giữ Django/DRF + Vue monorepo modular monolith                       | Accepted          | Không có lý do đổi stack; giảm rủi ro                                   |
| PROD-002 | Một chi nhánh, VND, timezone Asia/Bangkok                            | Accepted          | Khớp scope; schema vẫn tránh hardcode branch giả                        |
| PROD-003 | Django Groups cho 3 coarse role; permission/ownership ở BE           | Accepted          | Tận dụng auth hiện có, không thêm package sớm                           |
| PROD-004 | Order/payment là hai state machine tách biệt                         | Accepted          | Bảo vệ rule no-refund và manual transfer                                |
| PROD-005 | Reserve ở confirm; consume ở start preparation                       | Accepted          | Tránh oversell, khớp yêu cầu vận hành                                   |
| PROD-006 | Append-only stock/cash ledger; không hard-delete posted data         | Accepted          | Audit và báo cáo đáng tin cậy                                           |
| PROD-007 | Lot optional theo ingredient, FEFO; COGS từ consumed lot             | Accepted          | Hỗ trợ expiry và giá vốn từ sớm                                         |
| PROD-008 | Cash/manual transfer only; không refund/automatic gateway            | Accepted by scope | Không mở rộng sản phẩm                                                  |
| PROD-009 | Import sync có limit; document import tạo DRAFT                      | Accepted          | Không thêm queue sớm, bảo vệ ledger                                     |
| PROD-010 | Recommendation v1 rule/content/co-purchase trong monolith            | Accepted          | Có fallback, không cần LLM/microservice                                 |
| PROD-011 | Review unique per order line, sửa trong 7 ngày                       | Accepted          | Chống trùng, vẫn cho sửa lỗi hợp lý                                     |
| PROD-012 | Coffee designDNA kế thừa base component/token                        | Accepted          | Không rewrite UI; tách customer vs ops density                          |
| PROD-013 | Customer hero dùng ảnh thật + GSAP depth; không tải WebGL            | Accepted          | Giữ chiều sâu, giảm bundle và tránh lộ khung ảnh                        |
| PROD-014 | Không tính “lợi nhuận ròng” nếu thiếu overhead/đủ chi phí            | Accepted by scope | Tránh báo cáo gây hiểu sai                                              |
| PROD-015 | Compose `vubeo-coffee`, DB `vubeo_coffee`, host 5434/6381            | Accepted          | Cô lập container, volume và port khỏi project khác                      |
| PROD-016 | Money decimal 14,2; quantity 18,6; conversion 18,8                   | Accepted          | Không dùng float; đủ biên độ cho VND và định lượng                      |
| PROD-017 | `Idempotency-Key` cho create/action nhạy cảm                         | Accepted          | Retry không nhân đôi order/payment/ledger/import                        |
| PROD-018 | XLSX sync tối đa 5 MB/5.000 dòng, `__CLEAR__` khi update             | Accepted          | Giới hạn tài nguyên và semantics ô trống rõ                             |
| PROD-019 | Một reserved role group; employee có thêm duty groups                | Accepted          | Coarse role duy nhất, granular permission tái dùng                      |
| PROD-020 | Recipe tạo tiêu hao lý thuyết; kiểm kê/chứng từ xác nhận tồn thực tế | Accepted          | Nguyên liệu pha chế có hao hụt/yield, không được xem như hàng đếm chiếc |

## Input còn có thể bổ sung mà không chặn Phase 1

1. Tên thương hiệu hiển thị chính thức và logo/asset; nếu chưa có, dùng text mark/fallback trong Phase 1.
2. Danh sách ingredient bắt buộc theo lô sẽ được cấu hình ở Phase 2/3; cơ chế FEFO đã khóa.

Dark mode không thuộc MVP. Recommendation v1 không dùng ML cho tới khi đủ dữ liệu và có evaluation plan.

### PROD-020 — Tồn lý thuyết, tồn thực tế và đề xuất nhập

- Công thức là định mức tiêu hao chuẩn theo món/biến thể, dùng để ước tính nhu cầu, reservation, giá vốn
  chuẩn và đề xuất nhập; không phải bằng chứng rằng kho thực tế đã giảm chính xác đúng định lượng.
- Hệ thống phải phân biệt `estimated_on_hand` (tồn sổ/ước tính sau tiêu hao chuẩn) với số lượng kiểm kê
  thực tế. Nhập kho, kiểm kê, phiếu hao hụt và điều chỉnh đã POSTED là chứng từ xác nhận biến động vật lý.
- Chênh lệch giữa tiêu hao chuẩn và kiểm kê được ghi nhận là variance/hao hụt có audit; không sửa ngược
  công thức hoặc movement lịch sử để ép hai con số bằng nhau.
- “Khấu hao” không dùng cho nguyên liệu; thuật ngữ chuẩn là hao hụt định mức, hao hụt thực tế, tỷ lệ thu
  hồi (`yield`), hư hỏng, đổ bỏ và chênh lệch kiểm kê.
- Đề xuất nhập chỉ là quyết định hỗ trợ. Hệ thống không tự tạo/duyệt/POST phiếu nhập từ đề xuất.
