<script setup lang="ts">
import { useField, useForm } from "vee-validate";
import { ref } from "vue";

import { useToastStore } from "@/app/stores/toast";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import AppAlert from "@/components/feedback/AppAlert.vue";
import FormField from "@/components/form/FormField.vue";
import AuthLayout from "@/layouts/AuthLayout.vue";
import { toAppError } from "@/lib/http/errors";
import { registerSchema } from "@/modules/auth/schemas";

import { useAuth } from "../composables/useAuth";

const { register, loginLoading } = useAuth();
const toast = useToastStore();
const formError = ref("");
const { handleSubmit, setFieldError } = useForm({
  validationSchema: registerSchema,
  initialValues: { full_name: "", email: "", password: "", confirm_password: "" },
});
const { value: fullName, errorMessage: fullNameError } = useField<string>("full_name");
const { value: email, errorMessage: emailError } = useField<string>("email");
const { value: password, errorMessage: passwordError } = useField<string>("password");
const { value: confirmPassword, errorMessage: confirmPasswordError } =
  useField<string>("confirm_password");

const submit = handleSubmit(async (values) => {
  formError.value = "";
  try {
    await register({
      full_name: values.full_name,
      email: values.email,
      password: values.password,
    });
  } catch (error) {
    const appError = toAppError(error);
    toast.show(appError.message, "error");
    Object.entries(appError.fields).forEach(([field, message]) => {
      if (
        field === "full_name" ||
        field === "email" ||
        field === "password" ||
        field === "confirm_password"
      ) {
        setFieldError(field, message);
      }
    });
    if (Object.keys(appError.fields).length === 0) formError.value = appError.message;
  }
});
</script>

<template>
  <AuthLayout>
    <template #title>Tạo tài khoản</template>
    <template #subtitle>
      Đăng ký thành viên để đặt món và nhận ưu đãi tại Kim Thành Coffee.
    </template>

    <AppAlert v-if="formError" variant="error" title="Không thể đăng ký" class="mb-4">
      {{ formError }}
    </AppAlert>
    <form class="space-y-4" novalidate @submit="submit">
      <FormField v-slot="field" label="Họ và tên" name="full_name" :error="fullNameError" required>
        <BaseInput
          v-model="fullName"
          :id="field.id"
          name="full_name"
          autocomplete="name"
          :invalid="field.invalid"
          :aria-describedby="field.describedBy"
        />
      </FormField>
      <FormField v-slot="field" label="Email" name="email" :error="emailError" required>
        <BaseInput
          v-model="email"
          :id="field.id"
          name="email"
          type="email"
          autocomplete="email"
          :invalid="field.invalid"
          :aria-describedby="field.describedBy"
        />
      </FormField>
      <FormField v-slot="field" label="Mật khẩu" name="password" :error="passwordError" required>
        <BaseInput
          v-model="password"
          :id="field.id"
          name="password"
          type="password"
          autocomplete="new-password"
          :invalid="field.invalid"
          :aria-describedby="field.describedBy"
        />
      </FormField>
      <FormField
        v-slot="field"
        label="Nhập lại mật khẩu"
        name="confirm_password"
        :error="confirmPasswordError"
        required
      >
        <BaseInput
          v-model="confirmPassword"
          :id="field.id"
          name="confirm_password"
          type="password"
          autocomplete="new-password"
          :invalid="field.invalid"
          :aria-describedby="field.describedBy"
        />
      </FormField>
      <BaseButton type="submit" block :loading="loginLoading">Đăng ký</BaseButton>
    </form>
    <p class="mt-5 text-center text-sm text-[var(--color-text-muted)]">
      Đã có tài khoản?
      <RouterLink class="font-semibold text-[var(--color-primary)] hover:underline" to="/login">
        Đăng nhập
      </RouterLink>
    </p>
  </AuthLayout>
</template>
