from django.contrib.auth.models import Group

ROLE_ADMIN = "admin"
ROLE_EMPLOYEE = "employee"
ROLE_CUSTOMER = "customer"
ROLE_CHOICES = (ROLE_ADMIN, ROLE_EMPLOYEE, ROLE_CUSTOMER)
ROLE_GROUP_PREFIX = "role:"
ROLE_GROUP_NAMES = {role: f"{ROLE_GROUP_PREFIX}{role}" for role in ROLE_CHOICES}


def get_user_role(user) -> str:
    if user.is_superuser:
        return ROLE_ADMIN
    group_names = set(user.groups.values_list("name", flat=True))
    for role in ROLE_CHOICES:
        if ROLE_GROUP_NAMES[role] in group_names:
            return role
    return ROLE_CUSTOMER


def assign_role(*, user, role: str) -> None:
    if role not in ROLE_CHOICES:
        raise ValueError(f"Unknown role: {role}")
    role_groups = Group.objects.filter(name__startswith=ROLE_GROUP_PREFIX)
    target_group, _ = Group.objects.get_or_create(name=ROLE_GROUP_NAMES[role])
    user.groups.remove(*role_groups)
    user.groups.add(target_group)
