from decimal import Decimal

from django.db import migrations
from django.utils import timezone


def seed_inventory(apps, schema_editor):
    Unit = apps.get_model("inventory", "Unit")
    Ingredient = apps.get_model("inventory", "Ingredient")
    Supplier = apps.get_model("inventory", "Supplier")
    Recipe = apps.get_model("inventory", "Recipe")
    RecipeItem = apps.get_model("inventory", "RecipeItem")
    Variant = apps.get_model("catalog", "Variant")
    gram, _ = Unit.objects.update_or_create(code="g", defaults={"name": "Gram", "symbol": "g", "decimal_places": 3})
    ml, _ = Unit.objects.update_or_create(code="ml", defaults={"name": "Mililít", "symbol": "ml", "decimal_places": 3})
    coffee, _ = Ingredient.objects.update_or_create(code="robusta", defaults={"name": "Cà phê Robusta rang mộc", "base_unit": gram, "track_lot": True})
    cream, _ = Ingredient.objects.update_or_create(code="salt-cream", defaults={"name": "Kem muối tươi", "base_unit": ml, "track_lot": True})
    Supplier.objects.update_or_create(code="local-coffee", defaults={"name": "Nhà cung cấp cà phê địa phương", "contact_name": "Bộ phận bán hàng"})
    variant = Variant.objects.filter(code="kt-01-s").first()
    if variant and not Recipe.objects.filter(variant=variant, version=1).exists():
        recipe = Recipe.objects.create(variant=variant, version=1, effective_from=timezone.now())
        RecipeItem.objects.create(recipe=recipe, ingredient=coffee, quantity=Decimal("22"))
        RecipeItem.objects.create(recipe=recipe, ingredient=cream, quantity=Decimal("45"))


class Migration(migrations.Migration):
    dependencies = [("catalog", "0002_seed_demo_catalog"), ("inventory", "0001_initial")]
    operations = [migrations.RunPython(seed_inventory, migrations.RunPython.noop)]

