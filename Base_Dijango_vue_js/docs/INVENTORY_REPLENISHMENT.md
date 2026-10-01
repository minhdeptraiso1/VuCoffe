# Công thức tiêu hao và đề xuất nhập nguyên liệu

Trạng thái: quyết định kiến trúc đã duyệt; triển khai theo Phase 3, 5 và P08-S04. Tài liệu này là nguồn
thuật ngữ/công thức cho DB, API, UI, test và tài liệu nghiệp vụ về sau.

## Nguyên tắc

Recipe mô tả **định mức tiêu hao chuẩn** của một món/biến thể. Nguyên liệu pha chế không phải hàng đếm
chiếc: lượng sử dụng thật có thể lệch do cân đong, sơ chế, bay hơi, đổ bỏ, hư hỏng hoặc sai thao tác. Vì
vậy recipe không tự chứng minh tồn vật lý còn lại.

Không dùng “khấu hao” cho nguyên liệu. Dùng các thuật ngữ:

- Hao hụt định mức (`standard_loss_rate`).
- Tỷ lệ thu hồi (`yield_rate`).
- Hao hụt thực tế/wastage có chứng từ và lý do.
- Chênh lệch kiểm kê (`inventory_variance`).
- Tiêu hao chuẩn (`standard_consumption`).

## Ba số lượng phải tách biệt

| Khái niệm           | Ý nghĩa                                        | Nguồn                                                |
| ------------------- | ---------------------------------------------- | ---------------------------------------------------- |
| `estimated_on_hand` | Tồn sổ ước tính sau movement và tiêu hao chuẩn | receipt/adjustment/standard consumption              |
| `physical_count`    | Số lượng đếm thật tại một thời điểm            | stock count đã POSTED                                |
| `available`         | Lượng có thể hứa cho đơn mới                   | estimated on hand trừ reservation, có policy an toàn |

UI phải hiển thị nhãn và thời điểm nguồn; không gọi `estimated_on_hand` là “tồn thực tế”. Sau kiểm kê,
variance được POST bằng adjustment có audit, không sửa movement cũ.

## Công thức đề xuất

Với từng nguyên liệu và kỳ dự báo:

```text
standard_demand = Σ(forecast_variant_quantity × recipe_item_base_quantity)
loss_adjusted_demand = standard_demand × (1 + standard_loss_rate)
```

Nếu quản lý theo tỷ lệ thu hồi:

```text
gross_input_demand = standard_demand / yield_rate
```

Chỉ dùng một policy loss/yield đã cấu hình rõ để tránh tính hao hụt hai lần. Sau đó:

```text
raw_replenishment = gross_demand
                  + safety_stock
                  - available_stock
                  - confirmed_inbound_quantity

suggested_quantity = max(0, round_up_to_purchase_pack(raw_replenishment))
```

`confirmed_inbound_quantity` chỉ gồm phiếu mua/nhập đang chờ nhận ở trạng thái được policy chấp nhận;
không tính draft tùy tiện. Mọi phép tính dùng Decimal theo base unit và có `as_of` timestamp.

## Ví dụ

Dự báo 100 ly cà phê muối, mỗi ly 22 g cà phê:

```text
standard_demand = 100 × 22 = 2.200 g
loss_adjusted_demand (5%) = 2.200 × 1,05 = 2.310 g
raw_replenishment = 2.310 + 500 safety - 800 available - 300 inbound = 1.710 g
```

Nếu quy cách mua là túi 1 kg, đề xuất là 2 túi (2.000 g). Kết quả phải hiển thị breakdown này để người
quản lý hiểu và có thể bỏ qua; hệ thống không tự duyệt hoặc POST phiếu nhập.

## Dữ liệu cần có

- Recipe version/effective time và định lượng theo base unit.
- Completed order quantity theo đúng variant/recipe snapshot.
- Ingredient safety stock, loss hoặc yield policy.
- Supplier lead time, purchase pack size, minimum order quantity và supplier ưu tiên.
- Estimated stock, physical count gần nhất và thời điểm kiểm kê.
- Phiếu nhập đang chờ nhận đủ điều kiện tính inbound.
- Wastage/count variance lịch sử để hiệu chỉnh policy, không tự sửa recipe.

Thiếu physical count gần đây, recipe hoặc lead time phải tạo cảnh báo chất lượng dữ liệu và giảm độ tin cậy
của đề xuất; không âm thầm đưa ra con số có vẻ chính xác.

## Phân bổ theo phase

- **Phase 2:** recipe versioned và unit conversion; recipe là định mức chuẩn.
- **Phase 3:** receipt/lot/movement, estimated stock, reservation và nhãn phân biệt nguồn số lượng.
- **Phase 5:** thu completed order và recipe snapshot để có demand thực tế theo món.
- **Phase 8:** count/wastage/variance, standard COGS reconciliation và P08-S04 đề xuất nhập.
- **Phase 10:** dashboard/export theo dõi độ chính xác đề xuất và variance; không đổi transaction nguồn.

## Test bắt buộc khi triển khai

- Recipe đổi giữa kỳ phải dùng đúng version/effective time của từng order.
- Loss/yield không được tính hai lần; yield phải lớn hơn 0 và không vượt policy cho phép.
- Pending receipt, safety stock và pack rounding có golden fixture Decimal.
- Stock count stale, thiếu recipe hoặc thiếu physical count phải cảnh báo rõ.
- Cùng input/as-of phải cho kết quả deterministic và truy được reason breakdown.
- Tạo phiếu từ đề xuất chỉ tạo DRAFT, idempotent; không tự approve/POST hoặc thay đổi tồn.
