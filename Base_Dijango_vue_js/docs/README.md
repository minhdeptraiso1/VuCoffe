# Tài liệu dự án VuBeo Coffee

## Nguồn cần đọc theo thứ tự

1. `PROJECT_SCOPE.md` — phạm vi, role, luồng và invariant.
2. `BASE_AUDIT.md` — hiện trạng base và bằng chứng kiểm tra.
3. `DECISIONS.md` — quyết định/giả định cần duyệt.
4. `ARCHITECTURE.md` — module, model, state machine, transaction và FE architecture.
5. `INVENTORY_REPLENISHMENT.md` — tiêu hao chuẩn, tồn thực tế và công thức đề xuất nhập.
6. `DESIGN_DNA.md` + `COMPONENT_GUIDELINES.md` — thiết kế và UI gate.
7. `IMPORT_EXPORT_SPEC.md` — contract Excel.
8. `IMPLEMENTATION_PLAN.md` — roadmap Phase/Sprint/task/effort.
9. `PROGRESS.md` — nguồn tiến độ lần làm việc tiếp theo.

## Tài liệu base vẫn là nguồn chính thức

- `../AGENTS.md` và AGENTS theo thư mục.
- `standards/backend.md`, `standards/frontend.md`, `standards/api-contract.md`.
- `standards/architecture-decisions.md` cho ADR base.
- `../Base_dijango/docs/architecture.md` và `../frontend/docs/design-system.md` cho hiện trạng.

Không tạo `CODING_CONVENTIONS.md` mới vì AGENTS + `docs/standards/*` đã bao phủ convention và là nguồn
được source hiện tại tham chiếu. Khi product cần convention mới, cập nhật đúng standard/ADR thay vì tạo
hai nguồn mâu thuẫn.

## Cách bắt đầu/tiếp tục

- “Bắt đầu Phase X”: đọc `PROGRESS.md`, phase/sprint trong plan, kiểm tra repo thật rồi làm task sớm nhất.
- “Tiếp tục”: xác minh task chưa Done sớm nhất đủ dependency; không làm lại task đã có bằng chứng.
- Mỗi sprint dùng template trong `sprints/README.md`, cập nhật progress và kết quả gate.
