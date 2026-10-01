from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import APIException, ValidationError

from .models import Category, PriceHistory, Product, ProductTopping, Topping, Variant


class StaleCatalogVersion(APIException):
    status_code = 409
    default_detail = "Dữ liệu đã được cập nhật ở nơi khác. Vui lòng tải lại."
    default_code = "stale_version"


def _assert_version(instance, expected_version: int | None) -> None:
    if expected_version is not None and instance.version != expected_version:
        raise StaleCatalogVersion()


def save_category(*, instance: Category | None = None, **data) -> Category:
    if instance is None:
        return Category.objects.create(**data)
    _assert_version(instance, data.pop("version", None))
    for field, value in data.items():
        setattr(instance, field, value)
    instance.version += 1
    instance.save()
    return instance


def save_product(*, instance: Product | None = None, topping_ids=None, **data) -> Product:
    with transaction.atomic():
        if instance is None:
            product = Product.objects.create(**data)
        else:
            _assert_version(instance, data.pop("version", None))
            product = instance
            for field, value in data.items():
                setattr(product, field, value)
            product.version += 1
            product.save()
        if topping_ids is not None:
            ProductTopping.objects.filter(product=product).delete()
            ProductTopping.objects.bulk_create(
                [
                    ProductTopping(product=product, topping_id=topping_id)
                    for topping_id in topping_ids
                ]
            )
        return product


def save_variant(*, instance: Variant | None = None, **data) -> Variant:
    with transaction.atomic():
        if data.get("is_default"):
            product = data.get("product") or instance.product
            Variant.objects.filter(product=product, is_default=True).exclude(
                pk=getattr(instance, "pk", None)
            ).update(is_default=False)
        previous_price = instance.price if instance else None
        if instance is None:
            variant = Variant.objects.create(**data)
        else:
            _assert_version(instance, data.pop("version", None))
            variant = instance
            for field, value in data.items():
                setattr(variant, field, value)
            variant.version += 1
            variant.save()
        if previous_price != variant.price:
            PriceHistory.objects.create(
                item_type=PriceHistory.ItemType.VARIANT,
                item_code=variant.code,
                price=variant.price,
            )
        return variant


def save_topping(*, instance: Topping | None = None, **data) -> Topping:
    previous_price: Decimal | None = instance.price if instance else None
    if instance is None:
        topping = Topping.objects.create(**data)
    else:
        _assert_version(instance, data.pop("version", None))
        topping = instance
        for field, value in data.items():
            setattr(topping, field, value)
        topping.version += 1
        topping.save()
    if previous_price != topping.price:
        PriceHistory.objects.create(
            item_type=PriceHistory.ItemType.TOPPING,
            item_code=topping.code,
            price=topping.price,
        )
    return topping


def deactivate_catalog_item(*, instance) -> None:
    if isinstance(instance, Category) and instance.products.filter(is_active=True).exists():
        raise ValidationError({"is_active": "Không thể ẩn danh mục đang có món hoạt động."})
    instance.is_active = False
    instance.version += 1
    instance.save(update_fields=["is_active", "version", "updated_at"])
