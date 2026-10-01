from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet,
    PublicCustomizationView,
    PublicMenuDetailView,
    PublicMenuView,
    ToppingViewSet,
    VariantViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("variants", VariantViewSet, basename="variant")
router.register("toppings", ToppingViewSet, basename="topping")

urlpatterns = [
    path("", include(router.urls)),
    path("menu/", PublicMenuView.as_view(), name="public-menu"),
    path("menu/<slug:slug>/", PublicMenuDetailView.as_view(), name="public-menu-detail"),
    path(
        "menu/<slug:slug>/validate-customization/",
        PublicCustomizationView.as_view(),
        name="public-menu-customization",
    ),
]
