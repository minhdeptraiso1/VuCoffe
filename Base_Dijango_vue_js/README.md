# Base Django REST Framework + Vue.js

Repository mẫu gồm backend Django REST Framework và frontend Vue 3. Dự án dùng PostgreSQL, Redis,
JWT (refresh token trong cookie `HttpOnly`), CSRF, OpenAPI, TypeScript strict và các quality gate dùng
chung giữa local/CI.

## Cấu trúc repository

```text
.
├── Base_dijango/       # Django 5.2 + DRF
├── frontend/           # Vue 3 + TypeScript + Vite
├── docs/standards/     # Quy ước phát triển FE/BE/API
└── AGENTS.md           # Quy trình bắt buộc trước khi sửa code
```

> Tên thư mục `Base_dijango` được giữ nguyên để không làm hỏng đường dẫn/import hiện có.

## Yêu cầu

- Git.
- Python 3.12–3.14 và [uv](https://docs.astral.sh/uv/).
- Node.js 24 và pnpm 11.19.0 (nên bật qua Corepack).
- Docker Desktop để chạy PostgreSQL và Redis. Có thể dùng dịch vụ cài local nếu sửa `.env` tương ứng.

## Clone và chạy local

### 1. Clone repository

```powershell
git clone https://github.com/minhdeptraiso1/Base_Dijango_vue_js.git
cd Base_Dijango_vue_js
```

### 2. Khởi động PostgreSQL và Redis

```powershell
cd Base_dijango
docker compose up -d db redis
Copy-Item .env.example .env
```

Mở `Base_dijango/.env` và đổi hai dòng sau để khớp cổng Docker Compose:

```dotenv
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5434/vubeo_coffee
REDIS_URL=redis://127.0.0.1:6381/1
```

Compose project được cố định là `vubeo-coffee`, dùng volume riêng và không điều khiển container của các
repository Django khác. Host ports `5434`/`6381` cũng được tách khỏi base cũ dùng `5433`/`6380`.

Tạo hai secret khác nhau rồi thay vào `DJANGO_SECRET_KEY` và `JWT_SIGNING_KEY`:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Chạy lệnh trên hai lần. Không commit `.env`.

### 3. Cài và chạy backend

Vẫn tại thư mục `Base_dijango`:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Backend chạy tại <http://127.0.0.1:8000>. Khi `API_DOCS_ENABLED=true`, Swagger ở
<http://127.0.0.1:8000/api/docs/>.

### 4. Cài và chạy frontend

Mở terminal thứ hai tại root repository:

```powershell
cd frontend
corepack enable
corepack prepare pnpm@11.19.0 --activate
corepack pnpm --version
corepack pnpm install --frozen-lockfile
corepack pnpm dev
```

Lệnh kiểm tra phải in `11.19.0`. Trên Windows, nếu một bản `pnpm` cài global xuất hiện trước Corepack
trong `PATH`, tiếp tục dùng tiền tố `corepack pnpm` như trên để luôn tuân theo trường `packageManager`
trong `frontend/package.json`; không cần gỡ bản global chỉ để chạy repository này.

Mở <http://localhost:5173>. Các tài khoản dev được migration tạo khi backend chạy local:

- Admin: `admin@example.com` / `123456`
- Employee: `employee@example.com` / `123456`
- Customer: `customer@example.com` / `123456`

Vite proxy `/api` và `/health` sang backend cổng `8000`, vì vậy local mặc định không cần đặt
`VITE_API_BASE_URL`.

## Kiểm tra chất lượng

Backend (chạy trong `Base_dijango`):

```powershell
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\ruff.exe format --check .
.\.venv\Scripts\python.exe manage.py check --settings=config.settings.test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run --settings=config.settings.test
.\.venv\Scripts\pytest.exe
.\.venv\Scripts\python.exe manage.py spectacular --validate --fail-on-warn --file schema.yml --settings=config.settings.test
```

Frontend (chạy trong `frontend`):

```powershell
corepack pnpm typecheck
corepack pnpm lint
corepack pnpm format:check
corepack pnpm test
corepack pnpm build
```

E2E cần backend, frontend, PostgreSQL, Redis và user demo đang chạy:

```powershell
corepack pnpm exec playwright install chromium
corepack pnpm test:e2e
```

Repository ép line ending LF bằng `.gitattributes`. Sau khi pull thay đổi này vào một working tree Windows
cũ, chạy `git add --renormalize .` rồi xem kỹ `git diff --cached`; chỉ commit normalization trong commit
tooling riêng, không trộn với feature.

## Tài liệu phát triển

Trước khi sửa code, đọc [AGENTS.md](AGENTS.md) và file `AGENTS.md` trong phạm vi tương ứng:

- [Chuẩn frontend](docs/standards/frontend.md)
- [Chuẩn backend](docs/standards/backend.md)
- [Hợp đồng API](docs/standards/api-contract.md)
- [Quyết định kiến trúc](docs/standards/architecture-decisions.md)
- [Kiến trúc backend](Base_dijango/docs/architecture.md)
- [Design system frontend](frontend/docs/design-system.md)

## Đưa project hiện tại lên GitHub lần đầu

Chạy tại `D:\Project\Base\Base_djangi_vuejs` sau khi kiểm tra `.env` không được stage:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "chore: initialize Django Vue base repository"
git remote add origin https://github.com/minhdeptraiso1/Base_Dijango_vue_js.git
git push -u origin main
```

Nếu đã có remote `origin`, dùng:

```powershell
git remote set-url origin https://github.com/minhdeptraiso1/Base_Dijango_vue_js.git
git push -u origin main
```

Nếu GitHub báo remote đã có commit (ví dụ README tạo sẵn trên web), không dùng force push. Chạy
`git pull --rebase origin main`, xử lý conflict nếu có, rồi `git push -u origin main`.
