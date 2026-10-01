from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import QuerySet

from .roles import ROLE_EMPLOYEE, ROLE_GROUP_NAMES

User = get_user_model()
SYSTEM_PERMISSION_APPS = {"admin", "auth", "contenttypes", "sessions", "token_blacklist"}


def get_active_user_by_id(*, user_id: int) -> User | None:
    return User.objects.filter(id=user_id, is_active=True).first()


def get_employees() -> QuerySet:
    return (
        User.objects.filter(groups__name=ROLE_GROUP_NAMES[ROLE_EMPLOYEE])
        .prefetch_related("groups", "user_permissions__content_type")
        .distinct()
    )


def get_assignable_permissions() -> QuerySet[Permission]:
    return (
        Permission.objects.select_related("content_type")
        .exclude(content_type__app_label__in=SYSTEM_PERMISSION_APPS)
        .order_by("content_type__app_label", "codename")
    )
