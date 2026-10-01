from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations

TEST_USERS = (
    ("admin@example.com", "Quản trị viên Demo", "role:admin", True, True),
    ("employee@example.com", "Nhân viên Demo", "role:employee", True, False),
    ("customer@example.com", "Khách hàng Demo", "role:customer", False, False),
)


def seed_local_role_test_users(apps, schema_editor):
    if not settings.DEBUG:
        return

    Group = apps.get_model("auth", "Group")
    User = apps.get_model("accounts", "User")
    role_groups = {
        name: Group.objects.get_or_create(name=name)[0]
        for name in ("role:admin", "role:employee", "role:customer")
    }
    password = make_password(settings.DEMO_USER_PASSWORD)

    for email, full_name, role_name, is_staff, is_superuser in TEST_USERS:
        user, _ = User.objects.update_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "password": password,
                "is_active": True,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )
        user.groups.remove(*role_groups.values())
        user.groups.add(role_groups[role_name])


class Migration(migrations.Migration):
    dependencies = [("accounts", "0002_seed_role_groups")]
    operations = [migrations.RunPython(seed_local_role_test_users, migrations.RunPython.noop)]
