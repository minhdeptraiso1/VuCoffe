# Phạm vi sản phẩm — VuBeo Coffee

## Mục tiêu

Xây dựng web quản lý một cửa hàng cà phê, phục vụ khách đặt món và nhân viên vận hành từ menu tới đơn,
thanh toán, pha chế, kho, ca, thu chi, đánh giá, gợi ý và báo cáo. Mỗi chức năng được giao theo vertical
slice DB → API → UI → tích hợp → kiểm chứng.

## Vai trò và quyền cấp cao

| Năng lực                       |                CUSTOMER |                   EMPLOYEE |                           ADMIN |
| ------------------------------ | ----------------------: | -------------------------: | ------------------------------: |
| Đăng ký/đăng nhập/hồ sơ        |              Chính mình |                 Chính mình |        Mọi tài khoản theo quyền |
| Xem menu/tìm/lọc/gợi ý         |                      Có |                         Có |                              Có |
| Tạo đơn                        |            Đơn của mình |              POS cho khách |                              Có |
| Xem/hủy đơn                    | Sở hữu + đúng điều kiện |              Theo nhiệm vụ |     Toàn bộ, vẫn theo invariant |
| Xác nhận đơn/giữ kho           |                   Không |      `orders.accept_order` |                              Có |
| Thu ngân/xác nhận chuyển khoản |                   Không | `payments.confirm_payment` |                              Có |
| Pha chế/giao món               |                   Không |     `orders.prepare_order` |                              Có |
| Mở/đóng ca                     |                   Không |     `shifts.operate_shift` |                              Có |
| Danh mục/công thức/giá         |          Chỉ xem public |          Chỉ xem cần thiết |                         Quản lý |
| Nhập/kiểm kê/hao hụt           |                   Không |            Theo permission |                   Quản lý/duyệt |
| Thu chi                        |                   Không |            Theo permission |                   Quản lý/duyệt |
| Đánh giá                       |              Món đã mua |                        Xem | Ẩn/hiện, không sửa nội dung/sao |
| Import/export                  |                   Không |     Theo module/permission |                              Có |
| Dashboard                      |                   Không |           Phạm vi vận hành |                         Toàn bộ |

Role là lớp coarse-grained; employee có permission chi tiết theo nhiệm vụ. API luôn kiểm tra permission và
ownership/object scope. FE chỉ phản ánh quyền, không phải hàng rào bảo mật.

## Luồng chính

### Khách hàng

Đăng ký/đăng nhập → xem/tìm/lọc menu → chọn variant/topping/đường/đá → tạo đơn → nhân viên xác nhận và
giữ nguyên liệu → thanh toán → theo dõi pha chế/giao món → đơn hoàn thành → đánh giá.

### POS/nhân viên

Mở ca → chọn bàn hoặc mang đi → tạo/tiếp nhận đơn → kiểm tra khả năng phục vụ → xác nhận/giữ kho → thu
tiền hoặc xác nhận chuyển khoản → bắt đầu pha/trừ kho → đánh dấu sẵn sàng/giao → hoàn thành → đóng ca và
đối soát.

### Kho/tài chính

Danh mục nguyên liệu/nhà cung cấp/công thức → phiếu nhập nháp → duyệt/ghi sổ lô và tồn → reservation khi
nhận đơn → tiêu hao chuẩn khi bắt đầu pha → kiểm kê/hao hụt qua chứng từ duyệt → đối chiếu tồn ước tính với
tồn thực tế → đề xuất nhập theo nhu cầu → báo cáo từ ledger bất biến.

## Quy tắc bất biến

- `Order.status` và `payment_status` độc lập nhưng transition phải tương thích.
- Khách chỉ yêu cầu hủy khi chưa thanh toán và chưa bắt đầu pha; hủy/hết hạn giải phóng reservation.
- Đơn đã thanh toán không có cancel/refund trong bản này.
- Nhân viên xác nhận khả năng phục vụ trước khi nhận thanh toán.
- Chuyển khoản chỉ paid sau khi employee có quyền xác nhận; nút của khách không đủ bằng chứng.
- Reservation tạo atomically khi xác nhận đơn; standard consumption atomically khi bắt đầu pha. Đây là
  mức tiêu hao lý thuyết theo recipe snapshot, không thay thế kiểm kê thực tế.
- Nguyên liệu đã pha không tự cộng lại khi món/đơn lỗi; dùng phiếu hao hụt/điều chỉnh có audit.
- Tồn thực tế chỉ được xác nhận bởi chứng từ nhập/điều chỉnh/hao hụt và kiểm kê đã POSTED; chênh lệch với
  tồn ước tính phải được giữ làm variance có truy vết.
- Đề xuất nhập là dữ liệu hỗ trợ, không tự động tạo, duyệt hoặc POST chứng từ kho.
- Đơn, payment, stock movement, shift posting và voucher đã ghi sổ không hard-delete.
- Tiền dùng `Decimal`, currency VND; quantity dùng decimal theo base unit, không dùng float.
- Snapshot tên/giá/công thức/tax/discount cần thiết được lưu ở order line để lịch sử không đổi theo catalog.
- Tất cả action nhạy cảm có actor, timestamp, source và idempotency/concurrency guard.

## Trong phạm vi

- Một chi nhánh; khu vực/bàn; tại bàn và mang đi; kênh customer web/POS.
- Tiền mặt và chuyển khoản xác nhận thủ công.
- Catalog, variant, topping, option đường/đá, giá và recipe.
- Supplier, receipt, lot/expiry khi áp dụng, stock ledger/reservation/count/wastage.
- Shift, cash movement, income/expense voucher, reconciliation.
- Review/moderation, recommendation có fallback, analytics sự kiện cơ bản.
- Import/export XLSX theo module đã mô tả.
- Dashboard vận hành và báo cáo có công thức rõ.

## Ngoài phạm vi bản đầu

- Giao hàng, shipper, bản đồ.
- Refund/return/exchange/dispute/chargeback.
- Payroll, multi-branch, supplier debt/aging phức tạp.
- Automatic payment gateway/reconciliation ngân hàng.
- Voucher, loyalty, đặt bàn trước, QR gọi món.
- Native mobile app, offline-first POS, microservice, event broker, data warehouse.
- ML service/LLM bắt buộc; recommendation v1 có thể là rule/content-based.

## Backlog sau MVP

Voucher, điểm thưởng, booking, QR table ordering, refund workflow, multi-branch, supplier payable, payroll,
delivery, payment gateway, offline POS và recommendation ML chỉ được mở khi có yêu cầu/phạm vi riêng.

## Danh sách màn hình

### Public/CUSTOMER

Trang chủ/hero, menu, chi tiết món/customization, giỏ hàng, checkout/tạo đơn, hướng dẫn thanh toán, theo dõi
đơn, lịch sử/chi tiết đơn, đăng ký/đăng nhập, hồ sơ, gợi ý, tạo/sửa đánh giá.

### EMPLOYEE

POS, danh sách/chi tiết đơn, hàng đợi pha chế, bàn/khu vực, mở/đóng ca, thu tiền/xác nhận chuyển khoản,
phiếu nhập/kiểm kê/hao hụt/thu chi theo quyền, import preview/history và dashboard vận hành.

### ADMIN

Dashboard, user/employee permission, category/product/variant/topping/price, ingredient/unit/conversion,
supplier/recipe, receipt/stock ledger/reservation/count/wastage, area/table, shift/reconciliation,
income/expense, review moderation, recommendation config/metrics, import/export và audit history.

## Chỉ số thành công kỹ thuật

- Không có thao tác paid/posted/consumed lặp khi retry.
- Không oversell nguyên liệu trong các request xác nhận cạnh tranh được test.
- Mọi endpoint list có filter/sort/pagination allowlist và quyền scope.
- Critical E2E của ba role chạy qua API thật.
- UI critical usable bằng keyboard ở 375/768/1024/1440px và reduced motion.
- Báo cáo đối chiếu được với order/payment/stock/cash ledger nguồn.
