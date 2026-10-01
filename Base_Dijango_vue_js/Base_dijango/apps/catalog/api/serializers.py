from rest_framework import serializers

from apps.catalog.models import Category, Product, Topping, Variant


def detect_image_extension(uploaded_file) -> str | None:
    position = uploaded_file.tell()
    header = uploaded_file.read(16)
    uploaded_file.seek(position)
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if header.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        return ".webp"
    return None


class ProductImageUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, uploaded_file):
        if uploaded_file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Ảnh không được vượt quá 5 MB.")
        if detect_image_extension(uploaded_file) is None:
            raise serializers.ValidationError("Chỉ chấp nhận ảnh JPG, PNG hoặc WEBP.")
        return uploaded_file


class ProductImageUploadResponseSerializer(serializers.Serializer):
    image_url = serializers.URLField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "code",
            "name",
            "description",
            "display_order",
            "is_active",
            "version",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class VariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "product_name",
            "code",
            "name",
            "volume_ml",
            "price",
            "display_order",
            "is_default",
            "is_active",
            "no_stock_required",
            "version",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = [
            "id",
            "code",
            "name",
            "price",
            "is_active",
            "no_stock_required",
            "version",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    topping_ids = serializers.PrimaryKeyRelatedField(
        source="toppings", queryset=Topping.objects.all(), many=True, required=False
    )
    variants = VariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "code",
            "slug",
            "category",
            "name",
            "description",
            "image_url",
            "image_position",
            "tag",
            "is_featured",
            "is_best_seller",
            "is_new",
            "display_order",
            "is_active",
            "version",
            "updated_at",
            "variants",
            "topping_ids",
        ]
        read_only_fields = ["id", "updated_at", "variants"]


class PublicVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ["id", "code", "name", "volume_ml", "price", "is_default"]


class PublicToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ["id", "code", "name", "price"]


class PublicProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variants = PublicVariantSerializer(many=True, read_only=True)
    toppings = serializers.SerializerMethodField()
    sweetness_options = serializers.SerializerMethodField()
    ice_options = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "code",
            "slug",
            "category",
            "name",
            "description",
            "image_url",
            "image_position",
            "tag",
            "is_featured",
            "is_best_seller",
            "is_new",
            "variants",
            "toppings",
            "sweetness_options",
            "ice_options",
        ]

    def get_toppings(self, obj) -> list[dict]:
        values = [relation.topping for relation in obj.producttopping_set.all()]
        return PublicToppingSerializer(values, many=True).data

    def get_sweetness_options(self, obj) -> list[str]:
        if obj.category.code == "pastry":
            return []
        return ["100% đường", "70% đường", "50% đường", "30% đường", "Không đường"]

    def get_ice_options(self, obj) -> list[str]:
        if obj.category.code == "pastry":
            return []
        return ["100% đá", "50% đá", "Không đá", "Uống nóng"]


class CustomizationInputSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    topping_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list
    )
    sweetness = serializers.CharField(required=False, allow_blank=True, default="")
    ice = serializers.CharField(required=False, allow_blank=True, default="")
    quantity = serializers.IntegerField(min_value=1, max_value=99, default=1)


class CustomizationResultSerializer(serializers.Serializer):
    unit_price = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=14, decimal_places=2)
