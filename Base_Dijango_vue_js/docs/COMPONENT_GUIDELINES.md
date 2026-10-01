# Component guidelines

## Nguyên tắc

Trang nghiệp vụ chỉ ghép component chung/module component; native form controls nằm trong base component,
trừ ngoại lệ semantic được review. Không đưa HTTP/business rule vào shared UI. Props/emits có kiểu, slot
có contract, màu/spacing/radius dùng token.

Giữ và tiến hóa `BaseButton`, `BaseInput`, `BaseLabel`, `FormField`, `AppAlert`, `AppToast`, `AppLink`.
Trong Phase 1 có thể chuẩn hóa prefix thành `App*`, nhưng phải dùng compatibility export hoặc migrate theo
từng slice; không rename hàng loạt không giá trị.

## Bộ component mục tiêu

| Nhóm         | Component                                                                                                  |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| Action       | `AppButton`, `AppIconButton`, `AppLink`, `AppDropdownMenu`                                                 |
| Form         | `AppInput`, `AppTextarea`, `AppSelect`, `AppCombobox`, `AppCheckbox`, `AppRadio`, `AppSwitch`, `FormField` |
| Surface/data | `AppCard`, `AppStatCard`, `AppBadge`, `AppTabs`, `AppTable`, `AppPagination`, `AppFilterBar`               |
| Overlay      | `AppModal`, `AppDrawer`, `AppConfirmDialog`, `AppTooltip`                                                  |
| Feedback     | `AppAlert`, `AppToast`, `AppSpinner`, `AppSkeleton`, `AppEmptyState`, `AppErrorState`                      |
| Files        | `AppFileUpload`, `AppImportPreview`, `AppExportAction`                                                     |
| Domain shell | Customer header/cart shell, POS shell, employee/admin sidebar; không đưa domain vào base primitives        |

## Contract tối thiểu

- Variant/size/state tập trung; button có `type=button` mặc định và loading chặn submit lặp.
- Form control có label, unique ID, help/error `aria-describedby`, invalid/disabled/readonly.
- Modal/drawer có focus trap, Escape, focus return, scroll lock và accessible title.
- Table có caption/accessible header, loading/empty/error, sort state, pagination và mobile strategy.
- Confirm dialog mô tả hậu quả; destructive action không dùng màu làm tín hiệu duy nhất.
- File upload kiểm tra extension/size ở FE để phản hồi sớm nhưng BE vẫn kiểm tra lại.
- Import preview hiển thị tổng/new/update/error, lỗi row/column, filter lỗi và confirm idempotent.

## Showcase

Không mở route showcase trong sản phẩm. Trạng thái component được kiểm tra bằng unit test và màn hình
nghiệp vụ thật; dữ liệu tĩnh chỉ để kiểm tra component, không giả làm nghiệp vụ. Phải phủ:

- Tất cả variant/size/state, text dài, Vietnamese accents.
- Keyboard tab/shift-tab/enter/space/escape và focus return.
- 375/768/1024/1440 px; zoom 200%; reduced motion.
- Light palette chính, contrast và trạng thái success/warning/error/info.
- Overlay stacking, table overflow, form validation và loading/empty/error.

## Test strategy

- Vitest cho props/emits, keyboard, loading/disabled, ARIA và focus behavior.
- Visual/manual checklist trước khi dùng component trên nhiều page.
- Playwright cho overlay/form/table/import critical flows, không snapshot mọi pixel.
- Không đánh dấu component Done nếu showcase đẹp nhưng page thật chưa nối API hoặc thiếu error state.
