from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.accounts.roles import get_user_role
from apps.accounts.selectors import get_assignable_permissions

User = get_user_model()


class UserOutputSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "is_active",
            "date_joined",
            "role",
            "permissions",
        )
        read_only_fields = fields

    def get_role(self, obj) -> str:
        return get_user_role(obj)

    def get_permissions(self, obj) -> list[str]:
        return sorted(obj.get_all_permissions())


class RegisterInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    full_name = serializers.CharField(max_length=255, trim_whitespace=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_email(self, value: str) -> str:
        email = User.objects.normalize_email_address(value)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("Email này đã được sử dụng.", code="duplicate")
        return email

    def validate(self, attrs):
        candidate = User(email=attrs["email"], full_name=attrs["full_name"])
        try:
            validate_password(attrs["password"], user=candidate)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)}) from exc
        return attrs


class EmployeeInputSerializer(RegisterInputSerializer):
    pass


class PermissionInputSerializer(serializers.Serializer):
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=150), allow_empty=True, max_length=100
    )

    def validate_permissions(self, values: list[str]) -> list[Permission]:
        unique_values = sorted(set(values))
        found = {
            f"{permission.content_type.app_label}.{permission.codename}": permission
            for permission in get_assignable_permissions()
            if f"{permission.content_type.app_label}.{permission.codename}" in unique_values
        }
        missing = [value for value in unique_values if value not in found]
        if missing:
            raise serializers.ValidationError(
                f"Quyền không tồn tại: {', '.join(missing)}", code="invalid_permission"
            )
        return [found[value] for value in unique_values]


class PermissionOutputSerializer(serializers.Serializer):
    code = serializers.SerializerMethodField()
    name = serializers.CharField(read_only=True)

    def get_code(self, obj) -> str:
        return f"{obj.content_type.app_label}.{obj.codename}"


class LoginInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = User.objects.normalize_email_address(attrs["email"])
        user = authenticate(
            request=self.context.get("request"), email=email, password=attrs["password"]
        )
        if user is None or not user.is_active:
            raise AuthenticationFailed(
                "Email hoặc mật khẩu không hợp lệ.", code="invalid_credentials"
            )
        attrs["user"] = user
        return attrs


class LoginOutputSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    user = UserOutputSerializer(read_only=True)


class UpdateProfileInputSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, allow_blank=True, trim_whitespace=True)


class ActiveUserTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            token = RefreshToken(attrs["refresh"])
            user_id = token.get("user_id")
        except TokenError as exc:
            raise serializers.ValidationError(
                {"refresh": "Refresh token không hợp lệ hoặc đã hết hạn."}, code="token_not_valid"
            ) from exc
        if not User.objects.filter(id=user_id, is_active=True).exists():
            raise AuthenticationFailed("Tài khoản không hoạt động.", code="user_inactive")
        return super().validate(attrs)


class EmptyInputSerializer(serializers.Serializer):
    pass


class RefreshOutputSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)


class CsrfTokenOutputSerializer(serializers.Serializer):
    csrf_token = serializers.CharField(read_only=True)
