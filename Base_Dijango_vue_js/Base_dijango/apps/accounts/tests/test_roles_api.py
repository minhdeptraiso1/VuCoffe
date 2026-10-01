import pytest
from django.contrib.auth.models import Group, Permission

from apps.accounts.roles import ROLE_ADMIN, ROLE_CUSTOMER, ROLE_EMPLOYEE, assign_role
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_customer_can_register_and_receives_enriched_session(api_client):
    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "email": "Customer@Example.com",
            "full_name": "  Khách Hàng  ",
            "password": "StrongPass!123",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["user"]["email"] == "customer@example.com"
    assert response.data["user"]["full_name"] == "Khách Hàng"
    assert response.data["user"]["role"] == ROLE_CUSTOMER
    assert response.data["user"]["permissions"] == []
    assert response.data["access"]
    assert "refresh_token" in response.cookies


@pytest.mark.django_db
def test_registration_rejects_duplicate_email_case_insensitively(api_client):
    UserFactory(email="known@example.com")
    response = api_client.post(
        "/api/v1/auth/register/",
        {
            "email": "KNOWN@example.com",
            "full_name": "Duplicate",
            "password": "StrongPass!123",
        },
        format="json",
    )
    assert response.status_code == 400
    assert "email" in response.data["details"]


@pytest.mark.django_db
def test_only_admin_can_create_employee_and_grant_permissions(api_client):
    customer = UserFactory()
    assign_role(user=customer, role=ROLE_CUSTOMER)
    api_client.force_authenticate(customer)
    payload = {
        "email": "employee@example.com",
        "full_name": "Nhân viên",
        "password": "StrongPass!123",
    }
    assert api_client.post("/api/v1/auth/employees/", payload, format="json").status_code == 403

    admin = UserFactory(is_staff=True, is_superuser=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    api_client.force_authenticate(admin)
    created = api_client.post("/api/v1/auth/employees/", payload, format="json")
    assert created.status_code == 201
    assert created.data["role"] == ROLE_EMPLOYEE

    permission = Permission.objects.select_related("content_type").get(
        content_type__app_label="accounts", codename="view_user"
    )
    permission_name = f"{permission.content_type.app_label}.{permission.codename}"
    updated = api_client.patch(
        f"/api/v1/auth/employees/{created.data['id']}/permissions/",
        {"permissions": [permission_name]},
        format="json",
    )
    assert updated.status_code == 200
    assert updated.data["permissions"] == [permission_name]
    assert Group.objects.filter(name="role:employee", user=created.data["id"]).exists()


@pytest.mark.django_db
def test_admin_can_list_only_employees_and_assignable_permissions(api_client):
    admin = UserFactory(is_staff=True, is_superuser=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    employee = UserFactory(is_staff=True)
    assign_role(user=employee, role=ROLE_EMPLOYEE)
    UserFactory()

    api_client.force_authenticate(admin)
    employees = api_client.get("/api/v1/auth/employees/")
    assert employees.status_code == 200
    assert employees.data["count"] == 1
    assert [item["id"] for item in employees.data["results"]] == [employee.id]

    catalog = api_client.get("/api/v1/auth/permissions/")
    assert catalog.status_code == 200
    codes = {item["code"] for item in catalog.data}
    assert "accounts.view_user" in codes
    assert not any(code.startswith("auth.") for code in codes)


@pytest.mark.django_db
def test_non_admin_cannot_read_employee_or_permission_catalog(api_client):
    customer = UserFactory()
    assign_role(user=customer, role=ROLE_CUSTOMER)
    api_client.force_authenticate(customer)

    assert api_client.get("/api/v1/auth/employees/").status_code == 403
    assert api_client.get("/api/v1/auth/permissions/").status_code == 403


@pytest.mark.django_db
def test_revoked_employee_permission_disappears_from_me_on_next_request(api_client):
    admin = UserFactory(is_staff=True, is_superuser=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    employee = UserFactory(is_staff=True)
    assign_role(user=employee, role=ROLE_EMPLOYEE)
    permission = Permission.objects.get(content_type__app_label="accounts", codename="view_user")
    employee.user_permissions.add(permission)

    api_client.force_authenticate(employee)
    assert "accounts.view_user" in api_client.get("/api/v1/auth/me/").data["permissions"]

    api_client.force_authenticate(admin)
    revoked = api_client.patch(
        f"/api/v1/auth/employees/{employee.id}/permissions/",
        {"permissions": []},
        format="json",
    )
    assert revoked.status_code == 200
    assert revoked.data["permissions"] == []

    employee = type(employee).objects.get(id=employee.id)
    api_client.force_authenticate(employee)
    assert api_client.get("/api/v1/auth/me/").data["permissions"] == []


@pytest.mark.django_db
def test_system_permission_cannot_be_granted_to_employee(api_client):
    admin = UserFactory(is_staff=True, is_superuser=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    employee = UserFactory(is_staff=True)
    assign_role(user=employee, role=ROLE_EMPLOYEE)
    api_client.force_authenticate(admin)

    response = api_client.patch(
        f"/api/v1/auth/employees/{employee.id}/permissions/",
        {"permissions": ["auth.view_group"]},
        format="json",
    )
    assert response.status_code == 400
    assert "permissions" in response.data["details"]
