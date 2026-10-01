from rest_framework.permissions import BasePermission

from .roles import ROLE_ADMIN, ROLE_EMPLOYEE, get_user_role


class IsAdminRole(BasePermission):
    message = "Bạn cần quyền quản trị để thực hiện thao tác này."

    def has_permission(self, request, view) -> bool:
        return bool(request.user.is_authenticated and get_user_role(request.user) == ROLE_ADMIN)


class IsEmployeeOrAdminRole(BasePermission):
    message = "Chức năng này chỉ dành cho nhân viên hoặc quản trị viên."

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user.is_authenticated
            and get_user_role(request.user) in {ROLE_ADMIN, ROLE_EMPLOYEE}
        )
