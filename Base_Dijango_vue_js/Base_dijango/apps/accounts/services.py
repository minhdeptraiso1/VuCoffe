from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from .roles import ROLE_CUSTOMER, ROLE_EMPLOYEE, assign_role

User = get_user_model()


@transaction.atomic
def register_customer(*, email: str, full_name: str, password: str) -> User:
    normalized_email = User.objects.normalize_email_address(email)
    user = User(email=normalized_email, full_name=full_name.strip())
    validate_password(password, user=user)
    user.set_password(password)
    user.full_clean(exclude=["password"])
    user.save()
    assign_role(user=user, role=ROLE_CUSTOMER)
    return user


@transaction.atomic
def create_employee(*, email: str, full_name: str, password: str) -> User:
    normalized_email = User.objects.normalize_email_address(email)
    user = User(email=normalized_email, full_name=full_name.strip(), is_staff=True)
    validate_password(password, user=user)
    user.set_password(password)
    user.full_clean(exclude=["password"])
    user.save()
    assign_role(user=user, role=ROLE_EMPLOYEE)
    return user


@transaction.atomic
def set_employee_permissions(*, user: User, permissions: list[Permission]) -> User:
    assign_role(user=user, role=ROLE_EMPLOYEE)
    user.user_permissions.set(permissions)
    for cache_name in ("_perm_cache", "_user_perm_cache", "_group_perm_cache"):
        user.__dict__.pop(cache_name, None)
    return user


@transaction.atomic
def update_profile(*, user: User, full_name: str) -> User:
    user.full_name = full_name.strip()
    user.full_clean(exclude=["password"])
    user.save(update_fields=["full_name"])
    return user
