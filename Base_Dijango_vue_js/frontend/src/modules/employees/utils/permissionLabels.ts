const ACTION_LABELS: Record<string, string> = {
  add: "Thêm",
  change: "Cập nhật",
  delete: "Xóa",
  view: "Xem",
};

const MODEL_LABELS: Record<string, string> = {
  user: "tài khoản người dùng",
};

export function permissionLabel(code: string): string {
  const codename = code.split(".").at(-1) ?? code;
  const [action = "view", ...modelParts] = codename.split("_");
  const model = modelParts.join("_");
  const actionLabel = ACTION_LABELS[action] ?? "Sử dụng";
  const modelLabel = MODEL_LABELS[model] ?? "dữ liệu nghiệp vụ";
  return `${actionLabel} ${modelLabel}`;
}

export function permissionDescription(code: string): string {
  return `Cho phép ${permissionLabel(code).toLocaleLowerCase("vi-VN")} trong hệ thống.`;
}
