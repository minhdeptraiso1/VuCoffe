# P01-S02 — Registration, role/permission và layouts

**Trạng thái:** Done  
**Phase:** 1 — Design system, auth và layout

## Đã triển khai

- Data migration `accounts.0002_seed_role_groups` tạo ba reserved group và backfill user cũ.
- Data migration local-only `accounts.0003_seed_local_role_test_users` tạo account admin/employee/customer
  với password lấy từ `DEMO_USER_PASSWORD`; không chạy khi `DEBUG=False`.
- `POST /api/v1/auth/register/` tạo customer, login ngay và giữ refresh cookie HttpOnly.
- `/auth/me/` và login output thêm `role` cùng `permissions`.
- API admin tạo employee và đồng bộ granular Django permissions; backend trả 403 cho non-admin.
- API admin đọc danh sách employee có pagination và catalog assignable permissions; permission hệ thống
  bị loại ở cả catalog lẫn validation input.
- Frontend register form, role/permission route meta, guard, trang 403.
- Ba shell riêng: Customer, Employee và Admin; đăng nhập chuyển tới đúng surface.
- Management shell dùng sidebar trái; UI phân quyền hiển thị hoàn toàn bằng tiếng Việt.

## Bằng chứng

- Backend accounts và toàn suite: 30/30 test, coverage 92%; Ruff/check/migration/OpenAPI pass.
- Migration áp dụng thành công vào database `vubeo_coffee`; OpenAPI snapshot validate không warning.
- Đã xác minh `admin@example.com`, `employee@example.com`, `customer@example.com` có đúng role và mật khẩu
  local `123456` bằng Django password checker.
- E2E customer auth desktop/mobile pass.
- E2E backend thật xác minh customer → `/account`, admin → `/admin`, employee → `/employee`, sidebar
  quản lý và catalog phân quyền tiếng Việt.

## Acceptance đã chốt

- Backend đã có regression test revoke permission có hiệu lực ở request `/me` kế tiếp.
- UI quản trị tạo nhân viên/cấp quyền đã nối API thật; flow customer/admin/employee đã có E2E.
