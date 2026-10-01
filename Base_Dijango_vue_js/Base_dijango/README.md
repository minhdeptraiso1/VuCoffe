# Django Backend Base

Backend REST dạng modular monolith, dùng Django 5.2 LTS và Python 3.12. Django 5.2 được chọn vì là LTS;
DRF 3.16 hỗ trợ Django 5.2. Dependency chính và phụ được khóa trong `uv.lock`.

## Công nghệ

Django 5.2, Django REST Framework 3.16, PostgreSQL 18, Redis 8, Simple JWT 5.5,
drf-spectacular 0.29, django-environ, django-cors-headers, django-redis, Gunicorn và WhiteNoise.
Test dùng pytest/pytest-django/factory-boy; chất lượng mã dùng Ruff.

## Chạy dự án bằng VS Code và CMD

### 1. Chuẩn bị

Cần cài sẵn:

- Python 3.12 trở lên.
- PostgreSQL 18 đang chạy và đã có database `vubeo_coffee`.
- VS Code cùng extension **Python** của Microsoft.
- Redis local, hoặc Docker Desktop nếu muốn chạy Redis bằng Docker.

### 2. Mở dự án bằng VS Code

Mở **Command Prompt (CMD)**, sau đó chạy đúng thứ tự:

```cmd
cd /d D:\Project\Base\Base_dijango
code .
```

Trong VS Code:

1. Nhấn `Ctrl+Shift+P`.
2. Chọn `Python: Select Interpreter`.
3. Chọn file `D:\Project\Base\Base_dijango\.venv\Scripts\python.exe` nếu môi trường đã tồn tại.
4. Mở terminal từ menu **Terminal → New Terminal**.
5. Nhấn mũi tên cạnh nút dấu cộng của terminal và chọn **Command Prompt**.

Tất cả lệnh bên dưới được chạy trong terminal CMD của VS Code, tại thư mục gốc dự án.

### 3. Tạo và sửa file `.env`

```cmd
copy .env.example .env
notepad .env
```

Sửa thông tin kết nối PostgreSQL trong `.env`:

```dotenv
DATABASE_URL=postgresql://postgres:MAT_KHAU_POSTGRES@127.0.0.1:5432/vubeo_coffee
```

Nếu Redis được cài trực tiếp trên Windows và chạy ở cổng mặc định:

```dotenv
REDIS_URL=redis://127.0.0.1:6379/1
```

Nếu Redis chạy bằng Docker Compose của dự án:

```dotenv
REDIS_URL=redis://127.0.0.1:6381/1
```

Tạo hai secret riêng bằng lệnh sau, chạy hai lần và chép hai kết quả khác nhau vào
`DJANGO_SECRET_KEY` và `JWT_SIGNING_KEY`:

```cmd
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Không commit file `.env`. Nếu mật khẩu PostgreSQL chứa ký tự như `@`, `#`, `/` hoặc `:`, cần
URL-encode mật khẩu trước khi đưa vào `DATABASE_URL`.

### 4. Cài dependency

Nếu thư mục `.venv` đã tồn tại, kiểm tra Python của môi trường bằng:

```cmd
.\.venv\Scripts\python.exe --version
```

Nếu `.venv` chưa tồn tại, cài `uv` theo tài liệu chính thức rồi chạy `uv sync --frozen`. Sau đó môi trường
Python nằm tại `.venv\Scripts\python.exe`. Nếu VS Code chưa nhận ra, thực hiện lại bước
`Python: Select Interpreter`.

### 5. Khởi động Redis

Nếu Redis đã được cài và chạy trực tiếp trên Windows thì bỏ qua bước này.

Nếu dùng Docker, mở Docker Desktop, chờ Docker khởi động xong rồi chạy:

```cmd
docker compose up -d redis
docker compose ps
```

Redis Docker được ánh xạ ra cổng `6381`, vì vậy `.env` phải dùng
`REDIS_URL=redis://127.0.0.1:6381/1`.

### 6. Kiểm tra cấu hình và tạo bảng

Chạy lần lượt:

```cmd
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py showmigrations
```

- `check` kiểm tra cấu hình Django.
- `migrate` tạo/cập nhật bảng trong database `vubeo_coffee`.
- `showmigrations` hiển thị migration đã được áp dụng; migration có `[X]` là đã chạy.

### 7. Tài khoản demo theo role

Migration `accounts.0003_seed_local_role_test_users` tạo ba tài khoản dưới đây khi `DEBUG=True`. Migration
không tạo credential ở production (`DEBUG=False`):

| Role     | Email                  | Mật khẩu |
| -------- | ---------------------- | -------- |
| Admin    | `admin@example.com`    | `123456` |
| Employee | `employee@example.com` | `123456` |
| Customer | `customer@example.com` | `123456` |

Mật khẩu lấy từ `DEMO_USER_PASSWORD` trong `.env` và được hash bằng password hasher của Django. Ba tài
khoản chỉ phục vụ local/test, tuyệt đối không dùng ở production.

Lệnh seed cũ vẫn được giữ để tạo thêm `demo@example.com` nếu cần:

```cmd
.\.venv\Scripts\python.exe manage.py seed_dev_user
```

Lệnh có tính idempotent: nếu user đã tồn tại thì không tạo trùng và không tự đổi mật khẩu. Muốn đặt lại
mật khẩu theo `DEMO_USER_PASSWORD` trong `.env`, chạy:

```cmd
.\.venv\Scripts\python.exe manage.py seed_dev_user --reset-password
```

Có thể đổi `DEMO_USER_EMAIL` và `DEMO_USER_PASSWORD` trong `.env`. Lệnh bị vô hiệu hóa khi
`DEBUG=False`, vì vậy không tạo credential demo trong production. `123456` là mật khẩu yếu, chỉ dùng để
thử local. Django lưu password hash bằng `set_password()`, không lưu chuỗi `123456` trực tiếp trong DB.

### 8. Tạo tài khoản quản trị

Đây là bước tùy chọn, chỉ cần khi muốn đăng nhập Django Admin:

```cmd
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Nhập email và mật khẩu theo hướng dẫn trên terminal.

### 9. Chạy backend

```cmd
.\.venv\Scripts\python.exe manage.py runserver
```

Hoặc chạy qua `uv` đã cài trong môi trường dự án:

```cmd
.\.venv\Scripts\uv.exe run python manage.py runserver
```

Thư mục hiện tại không có môi trường `.tools`; vì vậy lệnh `.\.tools\Scripts\uv.exe ...` sẽ báo
`CommandNotFoundException`. Hãy dùng `.venv` như hai lệnh trên.

Phase 2 bổ sung migration cho catalog, nguyên liệu/công thức và import–export. Sau khi cập nhật code,
luôn chạy trước:

```cmd
.\.venv\Scripts\uv.exe run python manage.py migrate
```

Không đóng terminal đang chạy server. Nhấn `Ctrl+C` khi muốn dừng.

Các địa chỉ sử dụng:

- Swagger: <http://127.0.0.1:8000/api/docs/>
- ReDoc: <http://127.0.0.1:8000/api/redoc/>
- Django Admin: <http://127.0.0.1:8000/admin/>
- Liveness: <http://127.0.0.1:8000/health/live/>
- Readiness PostgreSQL/Redis: <http://127.0.0.1:8000/health/ready/>

### 10. Những lần chạy sau

Mở VS Code và chạy lại dự án bằng CMD:

```cmd
cd /d D:\Project\Base\Base_dijango
code .
docker compose up -d redis
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Có thể bỏ qua `docker compose up -d redis` nếu Redis local đã chạy. Không cần chạy lại `seed_dev_user`
hoặc `createsuperuser`, trừ khi muốn reset mật khẩu demo hay tạo thêm tài khoản quản trị.

### 11. Lỗi thường gặp

- `password authentication failed`: sửa user/mật khẩu trong `DATABASE_URL` của `.env`.
- `connection refused` ở cổng `5432`: kiểm tra PostgreSQL service đang chạy.
- Readiness báo Redis lỗi: kiểm tra `REDIS_URL`, Docker Desktop và `docker compose ps`.
- `'code' is not recognized`: mở dự án trực tiếp từ VS Code hoặc cài lệnh `code` vào PATH.
- Port `8000` đang được dùng: chạy `... manage.py runserver 8001` và truy cập cổng `8001`.

Schema OpenAPI: <http://127.0.0.1:8000/api/schema/>. Tài liệu API mở mặc định ở local và tắt mặc định
ở production.

## Chạy Docker

```powershell
docker compose up --build -d db redis
docker compose run --rm backend python manage.py migrate
docker compose run --rm backend python manage.py seed_dev_user
docker compose run --rm backend python manage.py createsuperuser
docker compose up --build backend
```

Compose project `vubeo-coffee` tạo database/Redis riêng trong named volumes (host ports 5434/6381),
không dùng chung container/volume với repository base khác. Container chạy non-root bằng Gunicorn; migration
là bước release riêng, không chạy trong mỗi worker. WhiteNoise phục vụ static đã `collectstatic` để Django
Admin hoạt động; media lớn nên đưa ra object storage/reverse proxy ở dự án cụ thể.

## Frontend và auth

Frontend Vue nằm trong thư mục `frontend`. Xem [hướng dẫn frontend](frontend/README.md) để chạy bằng
VS Code/CMD, kiểm thử và hiểu cấu trúc source.

Luồng auth không trả refresh token trong JSON. Backend đặt refresh token vào cookie `HttpOnly`; frontend
SPA giữ access token trong memory và gửi CSRF header cho login/refresh/logout. Axios tự refresh single-flight
và retry request 401 tối đa một lần. UI dùng toast cho phản hồi ngắn và confirm form/modal trước thao tác
nhạy cảm. Có thể thử nhanh qua giao diện:

```cmd
cd /d D:\Project\Base\Base_dijango\frontend
pnpm install --frozen-lockfile
pnpm dev
```

Mở <http://localhost:5173>, dùng một trong ba tài khoản role ở trên. Logout thu hồi refresh token trong cookie;
access token đã phát vẫn tồn tại đến khi hết hạn, nhưng frontend xóa nó khỏi memory ngay khi logout.
Chạy định kỳ `.\.venv\Scripts\python.exe manage.py flushexpiredtokens` (ví dụ cron hằng ngày).

## Kiểm tra

Test cần PostgreSQL riêng. Khi `DATABASE_URL` trỏ tới `vubeo_coffee`, Django pytest tạo/xóa
`test_vubeo_coffee`; Redis test dùng DB 15 và `REDIS_KEY_PREFIX` riêng. Không trỏ test vào tài khoản DB không
có quyền tạo database.

```powershell
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\ruff.exe format --check .
.\.venv\Scripts\python.exe manage.py check --settings=config.settings.test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run --settings=config.settings.test
.\.venv\Scripts\pytest.exe --cov --cov-report=term-missing
.\.venv\Scripts\python.exe manage.py spectacular --validate --fail-on-warn --file schema.yml --settings=config.settings.test
```

`makemigrations` sinh file mô tả thay đổi model; phải đọc và commit file đó. `migrate` áp các file chưa
chạy vào DB. Xem trạng thái bằng `showmigrations`. Trong môi trường dùng chung không sửa/xóa migration đã
chạy; tạo migration mới. Trước rollback (`migrate <app> <migration_trước>`), đọc reverse operation và
sao lưu DB vì data migration/xóa cột có thể không đảo ngược an toàn.

## Production

Dùng `config.settings.production`; các biến secret/DB/Redis/hosts/CORS/CSRF bắt buộc và thiếu sẽ fail fast.
Chỉ tin `X-Forwarded-Proto` khi ứng dụng nằm sau reverse proxy do mình kiểm soát. Bật HTTPS redirect,
secure cookies và HSTS; đặt CORS origin cụ thể. Schema/docs tắt trừ khi bật rõ ràng. DRF throttling dùng
Redis chia sẻ và nhận IP theo `REMOTE_ADDR`; reverse proxy phải ghi đè header từ client và truyền đúng IP.
Mặc định `DRF_NUM_PROXIES=0` nên throttle dùng `REMOTE_ADDR`. Sau reverse proxy, đặt đúng số proxy tin
cậy và cấu hình proxy ghi đè header do client gửi; cấu hình sai có thể gom mọi client hoặc cho giả IP.
Throttle hỗ trợ giảm tải, không thay thế rate limit ở edge, chống brute-force hay DDoS.

Giới hạn hiện tại: chưa có đổi/quên mật khẩu, MFA, social login, Celery/Kafka hoặc cơ
chế thu hồi toàn bộ JWT family. Xem thêm [tài liệu kiến trúc](docs/architecture.md).
