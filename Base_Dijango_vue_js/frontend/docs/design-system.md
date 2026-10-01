# Design system frontend

Thiết kế được rà soát theo workflow UI UX Pro Max với truy vấn cho cửa hàng cà phê một chi nhánh,
customer ordering, POS và admin responsive. Hướng chọn là **Warm Editorial Utility**: ấm, thủ công vừa
đủ ở customer surface nhưng vẫn rõ và dày thông tin ở POS/admin. Không có dark mode trong MVP.

- Màu: primary `#6F3F25`, nền `#F7F3EC`, surface `#FFFCF7`, text `#2B2118`, border `#D8C8B5`.
- Trạng thái: success `#2F6B45`, warning `#865708`, error `#A63D40`, info `#315E7A`; luôn kèm chữ.
- Chữ: Inter/system sans cho body; Georgia/system serif cho display heading đến khi có font brand.
- Khoảng cách: nhịp 4/8px; section 24–32px; control cao tối thiểu 44px.
- Bo góc: 8/12/20px; shadow nâu rất nhẹ để phân cấp surface.
- Focus: ring xanh 3px, không xóa outline nếu không có thay thế.
- Motion: 180–240ms cho hover/focus; tôn trọng `prefers-reduced-motion`.
- Layout: mobile-first từ 320px, kiểm tra chính ở 375/768/1024/1440px; content tối đa 1120px.

Token nguồn nằm ở `src/assets/styles/tokens.css`. Mọi button/input/label/error dùng component trong
`src/components`; biến thể mới phải mở rộng prop `variant`/`size`, không sao chép nhóm class sang page.
Route showcase `/design-system` đã được gỡ khỏi sản phẩm. Bộ token và component dùng chung vẫn được
duy trì trong source, kiểm tra bằng unit test và các màn hình nghiệp vụ thực tế.
