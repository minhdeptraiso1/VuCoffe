from django.conf import settings
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import permissions, status
from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import APIException, AuthenticationFailed, PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.accounts.permissions import IsAdminRole
from apps.accounts.roles import ROLE_EMPLOYEE, ROLE_GROUP_NAMES
from apps.accounts.selectors import get_assignable_permissions, get_employees
from apps.accounts.services import (
    create_employee,
    register_customer,
    set_employee_permissions,
    update_profile,
)
from common.exceptions import api_exception_handler

from .cookies import delete_refresh_cookie, prevent_sensitive_response_caching, set_refresh_cookie
from .serializers import (
    ActiveUserTokenRefreshSerializer,
    CsrfTokenOutputSerializer,
    EmployeeInputSerializer,
    EmptyInputSerializer,
    LoginInputSerializer,
    LoginOutputSerializer,
    PermissionInputSerializer,
    PermissionOutputSerializer,
    RefreshOutputSerializer,
    RegisterInputSerializer,
    UpdateProfileInputSerializer,
    UserOutputSerializer,
)

User = get_user_model()


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class RefreshThrottle(AnonRateThrottle):
    scope = "refresh"


def _dummy_get_response(request):
    return None


class EnforceCSRFMixin:
    def initial(self, request, *args, **kwargs) -> None:
        check = CSRFCheck(_dummy_get_response)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise PermissionDenied(f"CSRF Failed: {reason}", code="csrf_failed")
        super().initial(request, *args, **kwargs)


class CsrfTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Authentication"], responses={200: CsrfTokenOutputSerializer})
    def get(self, request):
        response = Response({"csrf_token": get_token(request._request)})
        return prevent_sensitive_response_caching(response)


class LoginView(EnforceCSRFMixin, APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [LoginThrottle]

    def get_authenticate_header(self, request):
        return "Bearer"

    @extend_schema(
        tags=["Authentication"],
        request=LoginInputSerializer,
        responses={200: LoginOutputSerializer, 401: OpenApiResponse(description="Sai thông tin")},
    )
    def post(self, request):
        serializer = LoginInputSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        output = {
            "access": str(refresh.access_token),
            "user": UserOutputSerializer(user).data,
        }
        response = Response(output)
        set_refresh_cookie(response, str(refresh))
        return prevent_sensitive_response_caching(response)


class RegisterView(EnforceCSRFMixin, APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [LoginThrottle]

    @extend_schema(
        tags=["Authentication"],
        request=RegisterInputSerializer,
        responses={201: LoginOutputSerializer},
    )
    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = register_customer(**serializer.validated_data)
        refresh = RefreshToken.for_user(user)
        response = Response(
            {"access": str(refresh.access_token), "user": UserOutputSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )
        set_refresh_cookie(response, str(refresh))
        return prevent_sensitive_response_caching(response)


class RefreshView(EnforceCSRFMixin, APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [RefreshThrottle]

    def get_authenticate_header(self, request):
        return "Bearer"

    @extend_schema(
        tags=["Authentication"],
        request=EmptyInputSerializer,
        responses={200: RefreshOutputSerializer},
    )
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)
        if not refresh_token:
            raise AuthenticationFailed("Không có phiên đăng nhập.", code="session_missing")

        serializer = ActiveUserTokenRefreshSerializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except APIException as exc:
            response = api_exception_handler(exc, {"request": request, "view": self})
            delete_refresh_cookie(response)
            return prevent_sensitive_response_caching(response)

        rotated_refresh = serializer.validated_data["refresh"]
        response = Response({"access": serializer.validated_data["access"]})
        set_refresh_cookie(response, rotated_refresh)
        return prevent_sensitive_response_caching(response)


class LogoutView(EnforceCSRFMixin, APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=["Authentication"],
        request=EmptyInputSerializer,
        responses={204: OpenApiResponse(description="Refresh token đã bị thu hồi")},
    )
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_NAME)
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except TokenError:
                pass
        response = Response(status=status.HTTP_204_NO_CONTENT)
        delete_refresh_cookie(response)
        return prevent_sensitive_response_caching(response)


class MeView(APIView):
    @extend_schema(tags=["Profile"], responses={200: UserOutputSerializer})
    def get(self, request):
        return Response(UserOutputSerializer(request.user).data)

    @extend_schema(
        tags=["Profile"],
        request=UpdateProfileInputSerializer,
        responses={200: UserOutputSerializer},
    )
    def patch(self, request):
        serializer = UpdateProfileInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = update_profile(user=request.user, **serializer.validated_data)
        return Response(UserOutputSerializer(user).data)


class EmployeeListView(GenericAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = UserOutputSerializer

    @extend_schema(tags=["Employees"], responses={200: UserOutputSerializer(many=True)})
    def get(self, request):
        employees = get_employees()
        page = self.paginate_queryset(employees)
        if page is not None:
            serializer = UserOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(UserOutputSerializer(employees, many=True).data)

    @extend_schema(
        tags=["Employees"],
        request=EmployeeInputSerializer,
        responses={201: UserOutputSerializer},
    )
    def post(self, request):
        serializer = EmployeeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_employee(**serializer.validated_data)
        return Response(UserOutputSerializer(user).data, status=status.HTTP_201_CREATED)


class PermissionCatalogView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(tags=["Employees"], responses={200: PermissionOutputSerializer(many=True)})
    def get(self, request):
        return Response(PermissionOutputSerializer(get_assignable_permissions(), many=True).data)


class EmployeePermissionView(APIView):
    permission_classes = [IsAdminRole]

    @extend_schema(
        tags=["Employees"],
        request=PermissionInputSerializer,
        responses={200: UserOutputSerializer},
    )
    def patch(self, request, user_id: int):
        user = get_object_or_404(
            User,
            id=user_id,
            groups__name=ROLE_GROUP_NAMES[ROLE_EMPLOYEE],
        )
        serializer = PermissionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = set_employee_permissions(
            user=user, permissions=serializer.validated_data["permissions"]
        )
        return Response(UserOutputSerializer(user).data)
