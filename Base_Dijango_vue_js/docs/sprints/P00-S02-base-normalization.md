# P00-S02 — Tooling và base normalization

Status: Done

## Mục tiêu và dependency

Làm cho quality gate local/CI ổn định trên Windows và Linux mà không đổi runtime behavior. Sprint bắt đầu
sau P00-S01; không triển khai domain cà phê.

## Task checklist

- [x] P00-S02-BASE01 — Phân tích working tree, line ending và tool versions.
- [x] P00-S02-BE01 — Giữ regression assertion cookie và format đúng Ruff.
- [x] P00-S02-FE01 — Thêm Git/Prettier LF policy.
- [x] P00-S02-TOOL01 — Chuẩn bị pnpm 11.19.0 qua Corepack và xác minh cách gọi.
- [x] P00-S02-DOC01 — Cập nhật hướng dẫn Windows/tooling.
- [x] P00-S02-DB01 — Tách Compose `vubeo-coffee`, DB/Redis/volume/ports khỏi project base khác.
- [x] P00-S02-QA01 — Chạy toàn bộ backend/frontend gates.
- [x] P00-S02-QA02 — Chạy E2E auth desktop/mobile và schema diff check.
- [x] P00-S02-PROG01 — Cập nhật progress/evidence và task tiếp theo.

## API/data/state contract

Không đổi API, database, migration, auth state hoặc schema OpenAPI. Thay đổi test chỉ chuẩn hóa cách đọc
flag `secure` của Python `Morsel`: flag false được biểu diễn bằng chuỗi rỗng và cần ép `bool` khi so sánh.

## Acceptance criteria / DoD

- Git checkout mới giữ LF bất kể `core.autocrlf` global.
- pnpm project chạy đúng 11.19.0 qua Corepack; lockfile không đổi.
- Ruff lint/format, Django checks, migration check, pytest, schema validation/diff pass.
- Typecheck, ESLint, Prettier, Vitest, build và Playwright pass.
- README nêu cách chạy Windows và troubleshooting; không có runtime dependency mới.

## Verification evidence

| Command/scenario                 | Result                                                      | Date/notes                            |
| -------------------------------- | ----------------------------------------------------------- | ------------------------------------- |
| Baseline audit                   | Prettier fail 59 file CRLF; Ruff format fail 1 changed test | 2026-09-18                            |
| `corepack pnpm --version`        | Pass: `11.19.0`                                             | Cache local `.tools`, ignored bởi Git |
| Ruff lint/format                 | Pass: 48 Python files formatted                             | 2026-09-18                            |
| Django check/migration check     | Pass; không có model change                                 | Database `vubeo_coffee`               |
| Pytest + coverage                | Pass: 23/23, tổng coverage 90%                              | PostgreSQL 5434, Redis 6381           |
| OpenAPI validation + schema diff | Pass; `schema.yml` không đổi                                | 2026-09-18                            |
| Typecheck/ESLint/Prettier        | Pass                                                        | pnpm 11.19.0                          |
| Vitest/build                     | Pass: 10/10; 144 modules build                              | JS khoảng 258 kB trước gzip           |
| Health live/ready                | Pass: 200; database/redis true                              | Compose `vubeo-coffee`                |
| Playwright                       | Pass: desktop + mobile Chromium, 2/2                        | API thật, không mock                  |

## Risks, decisions, known issues

- `pnpm` đầu PATH trong Codex là runtime fallback 12.4.1; project dựa vào Corepack/packageManager 11.19.0.
- Docker Compose project trước đây đụng tên `base_dijango` của repo khác. Đã cố định `vubeo-coffee`, DB
  `vubeo_coffee`, host ports 5434/6381 và volume riêng; project cũ không bị dừng/xóa.
- Không chạy format backend/frontend song song với feature khác để tránh diff khó review.

## Demo script

Hiển thị tool versions, chạy check backend/frontend, chạy E2E auth và xác nhận `git diff` không có schema
hoặc lockfile thay đổi ngoài dự kiến.
