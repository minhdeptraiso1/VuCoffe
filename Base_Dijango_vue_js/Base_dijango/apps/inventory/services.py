from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Recipe, RecipeItem, UnitConversion


def save_master(instance=None, **data):
    model = data.pop("model", None)
    if instance is None:
        if model is None:
            raise ValueError("model is required")
        return model.objects.create(**data)
    expected_version = data.pop("version", None)
    if expected_version is not None and instance.version != expected_version:
        raise ValidationError({"version": "Dữ liệu đã thay đổi. Vui lòng tải lại."}, code="stale")
    for field, value in data.items():
        setattr(instance, field, value)
    instance.version += 1
    instance.save()
    return instance


def _conversion_reaches(
    start_id: int, target_id: int, seen: set[int], excluded_id: int | None = None
) -> bool:
    if start_id == target_id:
        return True
    if start_id in seen:
        return False
    seen.add(start_id)
    conversions = UnitConversion.objects.filter(from_unit_id=start_id)
    if excluded_id:
        conversions = conversions.exclude(pk=excluded_id)
    next_ids = conversions.values_list("to_unit_id", flat=True)
    return any(_conversion_reaches(unit_id, target_id, seen, excluded_id) for unit_id in next_ids)


def save_conversion(*, instance: UnitConversion | None = None, **data) -> UnitConversion:
    from_unit = data.get("from_unit", instance.from_unit if instance else None)
    to_unit = data.get("to_unit", instance.to_unit if instance else None)
    if from_unit == to_unit:
        raise ValidationError({"to_unit": "Đơn vị nguồn và đích phải khác nhau."})
    if _conversion_reaches(to_unit.id, from_unit.id, set(), instance.pk if instance else None):
        raise ValidationError({"to_unit": "Quy đổi này tạo thành vòng lặp."})
    if instance is None:
        return UnitConversion.objects.create(**data)
    for field, value in data.items():
        setattr(instance, field, value)
    instance.save()
    return instance


@transaction.atomic
def create_recipe(*, variant=None, topping=None, items: list[dict], effective_from=None) -> Recipe:
    if bool(variant) == bool(topping):
        raise ValidationError("Công thức phải thuộc đúng một biến thể hoặc món thêm.")
    target_filter = {"variant": variant} if variant else {"topping": topping}
    previous = Recipe.objects.select_for_update().filter(**target_filter)
    next_version = (
        previous.order_by("-version").values_list("version", flat=True).first() or 0
    ) + 1
    previous.update(is_active=False)
    recipe = Recipe.objects.create(
        variant=variant,
        topping=topping,
        version=next_version,
        effective_from=effective_from or timezone.now(),
    )
    if not items:
        raise ValidationError({"items": "Công thức cần ít nhất một nguyên liệu."})
    RecipeItem.objects.bulk_create([RecipeItem(recipe=recipe, **item) for item in items])
    return recipe
