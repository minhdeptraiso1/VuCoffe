from decimal import Decimal
from uuid import uuid4

from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminRole
from apps.catalog.models import Category, Product, Topping, Variant
from apps.catalog.selectors import get_public_menu
from apps.catalog.services import (
    deactivate_catalog_item,
    save_category,
    save_product,
    save_topping,
    save_variant,
)

from .serializers import (
    CategorySerializer,
    CustomizationInputSerializer,
    CustomizationResultSerializer,
    ProductImageUploadResponseSerializer,
    ProductImageUploadSerializer,
    ProductSerializer,
    PublicProductSerializer,
    ToppingSerializer,
    VariantSerializer,
    detect_image_extension,
)


class AdminCatalogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["name", "code", "display_order", "updated_at"]
    ordering = ["display_order", "name"]
    search_fields = ["name", "code"]
    http_method_names = ["get", "post", "patch", "head", "options"]

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        deactivate_catalog_item(instance=instance)
        return Response(self.get_serializer(instance).data)


@extend_schema_view(
    list=extend_schema(tags=["Catalog admin"]), create=extend_schema(tags=["Catalog admin"])
)
class CategoryViewSet(AdminCatalogViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.instance = save_category(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = save_category(
            instance=serializer.instance, **serializer.validated_data
        )


@extend_schema_view(
    list=extend_schema(tags=["Catalog admin"]), create=extend_schema(tags=["Catalog admin"])
)
class ProductViewSet(AdminCatalogViewSet):
    queryset = Product.objects.select_related("category").prefetch_related("variants", "toppings")
    serializer_class = ProductSerializer
    ordering = ["category__display_order", "display_order", "name"]
    search_fields = ["name", "code", "description"]

    @extend_schema(
        tags=["Catalog admin"],
        request=ProductImageUploadSerializer,
        responses={201: ProductImageUploadResponseSerializer},
    )
    @action(
        detail=False, methods=["post"], url_path="upload-image", parser_classes=[MultiPartParser]
    )
    def upload_image(self, request):
        serializer = ProductImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        extension = detect_image_extension(uploaded_file)
        file_name = default_storage.save(
            f"catalog/products/{uuid4().hex}{extension}", uploaded_file
        )
        return Response(
            {"image_url": default_storage.url(file_name)}, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        toppings = serializer.validated_data.pop("toppings", None)
        serializer.instance = save_product(
            topping_ids=[item.id for item in toppings] if toppings is not None else None,
            **serializer.validated_data,
        )

    def perform_update(self, serializer):
        toppings = serializer.validated_data.pop("toppings", None)
        serializer.instance = save_product(
            instance=serializer.instance,
            topping_ids=[item.id for item in toppings] if toppings is not None else None,
            **serializer.validated_data,
        )


@extend_schema_view(
    list=extend_schema(tags=["Catalog admin"]), create=extend_schema(tags=["Catalog admin"])
)
class VariantViewSet(AdminCatalogViewSet):
    queryset = Variant.objects.select_related("product")
    serializer_class = VariantSerializer
    ordering = ["product", "display_order", "price"]

    def perform_create(self, serializer):
        serializer.instance = save_variant(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = save_variant(
            instance=serializer.instance, **serializer.validated_data
        )


@extend_schema_view(
    list=extend_schema(tags=["Catalog admin"]), create=extend_schema(tags=["Catalog admin"])
)
class ToppingViewSet(AdminCatalogViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    ordering_fields = ["name", "code", "price", "updated_at"]
    ordering = ["name"]

    def perform_create(self, serializer):
        serializer.instance = save_topping(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = save_topping(
            instance=serializer.instance, **serializer.validated_data
        )


class PublicMenuView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Public menu"], responses={200: PublicProductSerializer(many=True)})
    def get(self, request):
        products = get_public_menu(
            search=request.query_params.get("search", "").strip(),
            category=request.query_params.get("category", "").strip(),
        )
        return Response(PublicProductSerializer(products, many=True).data)


class PublicMenuDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Public menu"], responses={200: PublicProductSerializer})
    def get(self, request, slug: str):
        product = get_object_or_404(get_public_menu(), slug=slug)
        return Response(PublicProductSerializer(product).data, status=status.HTTP_200_OK)


class PublicCustomizationView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=["Public menu"],
        request=CustomizationInputSerializer,
        responses={200: CustomizationResultSerializer},
    )
    def post(self, request, slug: str):
        product = get_object_or_404(get_public_menu(), slug=slug)
        serializer = CustomizationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        variant = get_object_or_404(product.variants.filter(is_active=True), pk=data["variant_id"])
        allowed_toppings = {
            relation.topping_id: relation.topping for relation in product.producttopping_set.all()
        }
        requested_ids = set(data["topping_ids"])
        if not requested_ids.issubset(allowed_toppings):
            raise serializers.ValidationError(
                {"topping_ids": "Có món thêm không áp dụng cho sản phẩm này."}
            )
        public_data = PublicProductSerializer(product).data
        if data["sweetness"] and data["sweetness"] not in public_data["sweetness_options"]:
            raise serializers.ValidationError({"sweetness": "Mức đường không hợp lệ."})
        if data["ice"] and data["ice"] not in public_data["ice_options"]:
            raise serializers.ValidationError({"ice": "Lựa chọn đá không hợp lệ."})
        unit_price = variant.price + sum(
            (allowed_toppings[item_id].price for item_id in requested_ids), Decimal("0")
        )
        result = {
            "unit_price": unit_price,
            "total_price": unit_price * data["quantity"],
        }
        return Response(CustomizationResultSerializer(result).data)
