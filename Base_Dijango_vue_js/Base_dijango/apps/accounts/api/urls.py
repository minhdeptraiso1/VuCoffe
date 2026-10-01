from django.urls import path

from .views import (
    CsrfTokenView,
    EmployeeListView,
    EmployeePermissionView,
    LoginView,
    LogoutView,
    MeView,
    PermissionCatalogView,
    RefreshView,
    RegisterView,
)

app_name = "accounts_api"

urlpatterns = [
    path("csrf/", CsrfTokenView.as_view(), name="csrf"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", MeView.as_view(), name="me"),
    path("employees/", EmployeeListView.as_view(), name="employee-list"),
    path("permissions/", PermissionCatalogView.as_view(), name="permission-catalog"),
    path(
        "employees/<int:user_id>/permissions/",
        EmployeePermissionView.as_view(),
        name="employee-permissions",
    ),
]
