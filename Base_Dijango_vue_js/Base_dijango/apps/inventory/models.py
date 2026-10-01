from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from apps.catalog.models import Topping, Variant


class MasterDataModel(models.Model):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=140)
    is_active = models.BooleanField(default=True)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["name"]


class Unit(MasterDataModel):
    symbol = models.CharField(max_length=20)
    decimal_places = models.PositiveSmallIntegerField(default=3)

    def __str__(self) -> str:
        return self.symbol


class UnitConversion(models.Model):
    from_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="conversions_from")
    to_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="conversions_to")
    factor = models.DecimalField(
        max_digits=18,
        decimal_places=8,
        validators=[MinValueValidator(Decimal("0.00000001"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(from_unit=models.F("to_unit")),
                name="inventory_conversion_units_differ",
            ),
            models.UniqueConstraint(
                fields=["from_unit", "to_unit"], name="inventory_unique_unit_conversion"
            ),
        ]

    def __str__(self) -> str:
        return f"1 {self.from_unit} = {self.factor} {self.to_unit}"


class Ingredient(MasterDataModel):
    base_unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="ingredients")
    track_lot = models.BooleanField(default=False)
    minimum_level = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=0,
        validators=[MinValueValidator(Decimal("0"))],
    )

    def __str__(self) -> str:
        return self.name


class Supplier(MasterDataModel):
    contact_name = models.CharField(max_length=140, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    variant = models.ForeignKey(
        Variant, null=True, blank=True, on_delete=models.PROTECT, related_name="recipes"
    )
    topping = models.ForeignKey(
        Topping, null=True, blank=True, on_delete=models.PROTECT, related_name="recipes"
    )
    version = models.PositiveIntegerField()
    effective_from = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-effective_from", "-version"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(variant__isnull=False, topping__isnull=True)
                    | Q(variant__isnull=True, topping__isnull=False)
                ),
                name="inventory_recipe_exactly_one_target",
            ),
            models.UniqueConstraint(
                fields=["variant", "version"],
                condition=Q(variant__isnull=False),
                name="inventory_unique_variant_recipe_version",
            ),
            models.UniqueConstraint(
                fields=["topping", "version"],
                condition=Q(topping__isnull=False),
                name="inventory_unique_topping_recipe_version",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.variant or self.topping} · v{self.version}"


class RecipeItem(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="items")
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, related_name="recipe_items"
    )
    quantity = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        validators=[MinValueValidator(Decimal("0.000001"))],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="inventory_unique_recipe_ingredient"
            )
        ]

    def __str__(self) -> str:
        return f"{self.recipe} · {self.ingredient}"
