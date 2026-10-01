from decimal import Decimal

from django.db import migrations
from django.utils import timezone


def complete_demo_variant_recipes(apps, schema_editor):
    Ingredient = apps.get_model("inventory", "Ingredient")
    Recipe = apps.get_model("inventory", "Recipe")
    RecipeItem = apps.get_model("inventory", "RecipeItem")
    Variant = apps.get_model("catalog", "Variant")

    coffee = Ingredient.objects.filter(code="robusta").first()
    cream = Ingredient.objects.filter(code="salt-cream").first()
    if not coffee or not cream:
        return

    quantities = {
        "kt-01-s": (Decimal("22"), Decimal("45")),
        "kt-01-m": (Decimal("30"), Decimal("60")),
        "kt-01-l": (Decimal("38"), Decimal("75")),
    }
    for variant_code, (coffee_quantity, cream_quantity) in quantities.items():
        variant = Variant.objects.filter(code=variant_code).first()
        if not variant or Recipe.objects.filter(variant=variant, is_active=True).exists():
            continue
        recipe = Recipe.objects.create(
            variant=variant,
            version=1,
            effective_from=timezone.now(),
            is_active=True,
        )
        RecipeItem.objects.bulk_create(
            [
                RecipeItem(recipe=recipe, ingredient=coffee, quantity=coffee_quantity),
                RecipeItem(recipe=recipe, ingredient=cream, quantity=cream_quantity),
            ]
        )


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0003_alter_recipeitem_quantity_and_more"),
    ]

    operations = [
        migrations.RunPython(complete_demo_variant_recipes, migrations.RunPython.noop),
    ]
