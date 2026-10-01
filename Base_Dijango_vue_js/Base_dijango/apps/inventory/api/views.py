from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets

from apps.accounts.permissions import IsAdminRole
from apps.inventory.models import Ingredient, Recipe, Supplier, Unit, UnitConversion
from apps.inventory.services import save_conversion, save_master

from .serializers import (
    IngredientSerializer,
    RecipeSerializer,
    SupplierSerializer,
    UnitConversionSerializer,
    UnitSerializer,
)


class AdminMasterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["code", "name"]
    ordering_fields = ["code", "name", "updated_at"]
    ordering = ["name"]
    http_method_names = ["get", "post", "patch", "head", "options"]


@extend_schema_view(list=extend_schema(tags=["Inventory master"]))
class UnitViewSet(AdminMasterViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def perform_create(self, serializer):
        serializer.instance = save_master(model=Unit, **serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = save_master(instance=serializer.instance, **serializer.validated_data)


@extend_schema_view(list=extend_schema(tags=["Inventory master"]))
class UnitConversionViewSet(AdminMasterViewSet):
    queryset = UnitConversion.objects.select_related("from_unit", "to_unit")
    serializer_class = UnitConversionSerializer
    search_fields = []
    ordering_fields = ["id"]

    def perform_create(self, serializer):
        serializer.instance = save_conversion(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = save_conversion(
            instance=serializer.instance, **serializer.validated_data
        )


@extend_schema_view(list=extend_schema(tags=["Inventory master"]))
class IngredientViewSet(AdminMasterViewSet):
    queryset = Ingredient.objects.select_related("base_unit")
    serializer_class = IngredientSerializer

    def perform_create(self, serializer):
        serializer.instance = save_master(model=Ingredient, **serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = save_master(instance=serializer.instance, **serializer.validated_data)


@extend_schema_view(list=extend_schema(tags=["Inventory master"]))
class SupplierViewSet(AdminMasterViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def perform_create(self, serializer):
        serializer.instance = save_master(model=Supplier, **serializer.validated_data)

    def perform_update(self, serializer):
        serializer.instance = save_master(instance=serializer.instance, **serializer.validated_data)


@extend_schema_view(list=extend_schema(tags=["Recipes"]))
class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.select_related("variant__product", "topping").prefetch_related(
        "items__ingredient__base_unit"
    )
    http_method_names = ["get", "post", "head", "options"]
