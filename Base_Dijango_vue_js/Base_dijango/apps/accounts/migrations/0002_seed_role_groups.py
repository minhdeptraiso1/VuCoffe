from django.db import migrations

ROLE_GROUPS = ("role:admin", "role:employee", "role:customer")


def seed_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("accounts", "User")
    groups = {name: Group.objects.get_or_create(name=name)[0] for name in ROLE_GROUPS}
    for user in User.objects.all().iterator():
        role_name = "role:admin" if user.is_superuser else "role:customer"
        user.groups.remove(*groups.values())
        user.groups.add(groups[role_name])


def remove_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=ROLE_GROUPS).delete()


class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]
    operations = [migrations.RunPython(seed_roles, remove_roles)]
