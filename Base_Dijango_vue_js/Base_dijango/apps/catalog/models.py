from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class TimestampedVersionedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True


class Category(TimestampedVersionedModel):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Product(TimestampedVersionedModel):
    code = models.SlugField(max_length=50, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    image_url = models.CharField(max_length=500, blank=True)
    image_position = models.CharField(max_length=50, default="center center")
    tag = models.CharField(max_length=80, blank=True)
    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    toppings = models.ManyToManyField("Topping", through="ProductTopping", related_name="products")

    class Meta:
        ordering = ["category__display_order", "display_order", "name"]
        indexes = [models.Index(fields=["category", "is_active", "display_order"])]

    def __str__(self) -> str:
        return self.name


class Variant(TimestampedVersionedModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="variants")
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=80)
    volume_ml = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    display_order = models.PositiveSmallIntegerField(default=0)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    no_stock_required = models.BooleanField(default=False)

    class Meta:
        ordering = ["display_order", "price"]
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                condition=models.Q(is_default=True, is_active=True),
                name="catalog_one_active_default_variant",
            )
        ]

    def __str__(self) -> str:
        return f"{self.product.name} · {self.name}"


class Topping(TimestampedVersionedModel):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )
    is_active = models.BooleanField(default=True)
    no_stock_required = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ProductTopping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "topping"], name="catalog_unique_product_topping"
            )
        ]

    def __str__(self) -> str:
        return f"{self.product} · {self.topping}"


class PriceHistory(models.Model):
    class ItemType(models.TextChoices):
        VARIANT = "variant", "Biến thể"
        TOPPING = "topping", "Món thêm"

    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    item_code = models.SlugField(max_length=50)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    effective_from = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-effective_from"]
        indexes = [models.Index(fields=["item_type", "item_code", "effective_from"])]

    def __str__(self) -> str:
        return f"{self.item_code} · {self.price}"
