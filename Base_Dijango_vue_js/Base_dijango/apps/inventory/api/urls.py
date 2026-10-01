from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientViewSet,
    RecipeViewSet,
    SupplierViewSet,
    UnitConversionViewSet,
    UnitViewSet,
)

router = DefaultRouter()
router.register("units", UnitViewSet)
router.register("unit-conversions", UnitConversionViewSet)
router.register("ingredients", IngredientViewSet)
router.register("suppliers", SupplierViewSet)
router.register("recipes", RecipeViewSet)

urlpatterns = [path("", include(router.urls))]
