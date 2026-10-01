import { toTypedSchema } from "@vee-validate/zod";
import { z } from "zod";

export const loginValuesSchema = z.object({
  email: z.string().min(1, "Vui lòng nhập email.").email("Email chưa đúng định dạng."),
  password: z.string().min(1, "Vui lòng nhập mật khẩu."),
});

export const loginSchema = toTypedSchema(loginValuesSchema);

export const registerValuesSchema = z
  .object({
    full_name: z.string().trim().min(2, "Họ tên cần ít nhất 2 ký tự.").max(255),
    email: z.string().min(1, "Vui lòng nhập email.").email("Email chưa đúng định dạng."),
    password: z.string().min(8, "Mật khẩu cần ít nhất 8 ký tự."),
    confirm_password: z.string().min(1, "Vui lòng nhập lại mật khẩu."),
  })
  .refine((values) => values.password === values.confirm_password, {
    message: "Mật khẩu nhập lại chưa khớp.",
    path: ["confirm_password"],
  });

export const registerSchema = toTypedSchema(registerValuesSchema);
