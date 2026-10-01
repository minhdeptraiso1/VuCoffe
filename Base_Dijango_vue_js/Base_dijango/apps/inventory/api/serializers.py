from rest_framework import serializers

from apps.inventory.models import Ingredient, Recipe, RecipeItem, Supplier, Unit, UnitConversion
from apps.inventory.services import create_recipe


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "code", "name", "symbol", "decimal_places", "is_active", "version"]
        read_only_fields = ["id"]


class UnitConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitConversion
        fields = ["id", "from_unit", "to_unit", "factor"]
        read_only_fields = ["id"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            "id",
            "code",
            "name",
            "base_unit",
            "track_lot",
            "minimum_level",
            "is_active",
            "version",
        ]
        read_only_fields = ["id"]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            "id",
            "code",
            "name",
            "contact_name",
            "phone",
            "email",
            "address",
            "is_active",
            "version",
        ]
        read_only_fields = ["id"]


class RecipeItemSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source="ingredient.name", read_only=True)
    unit_symbol = serializers.CharField(source="ingredient.base_unit.symbol", read_only=True)

    class Meta:
        model = RecipeItem
        fields = ["ingredient", "ingredient_name", "unit_symbol", "quantity"]


class RecipeSerializer(serializers.ModelSerializer):
    items = RecipeItemSerializer(many=True)
    target_name = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "variant",
            "topping",
            "target_name",
            "version",
            "effective_from",
            "is_active",
            "items",
        ]
        read_only_fields = ["id", "version", "is_active", "target_name"]
        extra_kwargs = {"effective_from": {"required": False}}

    def validate(self, attrs):
        variant = attrs.get("variant")
        topping = attrs.get("topping")
        if bool(variant) == bool(topping):
            raise serializers.ValidationError(
                "Công thức phải thuộc đúng một biến thể hoặc món thêm."
            )
        items = attrs.get("items", [])
        if not items:
            raise serializers.ValidationError({"items": "Công thức cần ít nhất một nguyên liệu."})
        ingredient_ids = [item["ingredient"].id for item in items]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                {"items": "Mỗi nguyên liệu chỉ được xuất hiện một lần."}
            )
        return attrs

    def get_target_name(self, obj) -> str:
        return str(obj.variant or obj.topping)

    def create(self, validated_data):
        items = validated_data.pop("items")
        return create_recipe(items=items, **validated_data)
