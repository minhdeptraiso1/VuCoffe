from django.db.models import Prefetch, Q, QuerySet

from .models import Category, Product, ProductTopping, Topping, Variant


def get_public_menu(*, search: str = "", category: str = "") -> QuerySet[Product]:
    products = Product.objects.filter(is_active=True, category__is_active=True)
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
    if category:
        products = products.filter(category__code=category)
    return products.select_related("category").prefetch_related(
        Prefetch("variants", queryset=Variant.objects.filter(is_active=True)),
        Prefetch(
            "producttopping_set",
            queryset=ProductTopping.objects.select_related("topping").filter(
                topping__is_active=True
            ),
        ),
    )


def get_public_product(*, slug: str) -> Product:
    return get_public_menu().get(slug=slug)


def get_active_toppings() -> QuerySet[Topping]:
    return Topping.objects.filter(is_active=True)


def get_active_categories() -> QuerySet[Category]:
    return Category.objects.filter(is_active=True)
