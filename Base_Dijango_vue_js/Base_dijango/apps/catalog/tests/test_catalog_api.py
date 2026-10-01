import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.accounts.roles import ROLE_ADMIN, ROLE_CUSTOMER, assign_role
from apps.accounts.tests.factories import UserFactory
from apps.catalog.models import Category, Product, Topping, Variant


@pytest.mark.django_db
def test_public_menu_only_returns_active_catalog(api_client):
    category = Category.objects.create(code="test-coffee", name="Cà phê")
    product = Product.objects.create(
        code="coffee-milk",
        slug="coffee-milk",
        category=category,
        name="Cà phê sữa",
        is_active=True,
    )
    Variant.objects.create(
        product=product,
        code="coffee-milk-s",
        name="S",
        price="32000",
        is_default=True,
    )
    Product.objects.create(
        code="hidden",
        slug="hidden",
        category=category,
        name="Món ẩn",
        is_active=False,
    )

    response = api_client.get("/api/v1/menu/?search=sữa")

    assert response.status_code == 200
    by_code = {item["code"]: item for item in response.data}
    assert "coffee-milk" in by_code
    assert "hidden" not in by_code
    assert by_code["coffee-milk"]["variants"][0]["price"] == "32000.00"


@pytest.mark.django_db
def test_only_admin_can_manage_catalog_and_stale_version_returns_conflict(api_client):
    customer = UserFactory()
    assign_role(user=customer, role=ROLE_CUSTOMER)
    api_client.force_authenticate(customer)
    assert (
        api_client.post("/api/v1/categories/", {"code": "test-tea", "name": "Trà"}).status_code
        == 403
    )

    admin = UserFactory(is_superuser=True, is_staff=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    api_client.force_authenticate(admin)
    created = api_client.post(
        "/api/v1/categories/",
        {"code": "test-tea", "name": "Trà", "display_order": 1},
        format="json",
    )
    assert created.status_code == 201

    updated = api_client.patch(
        f"/api/v1/categories/{created.data['id']}/",
        {"name": "Trà trái cây", "version": created.data["version"]},
        format="json",
    )
    assert updated.status_code == 200
    stale = api_client.patch(
        f"/api/v1/categories/{created.data['id']}/",
        {"name": "Tên cũ", "version": created.data["version"]},
        format="json",
    )
    assert stale.status_code == 409


@pytest.mark.django_db
def test_admin_can_create_product_variant_and_topping_allowlist(api_client):
    admin = UserFactory(is_superuser=True, is_staff=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    api_client.force_authenticate(admin)
    category = Category.objects.create(code="test-modern", name="Cà phê")
    topping = Topping.objects.create(code="test-cream", name="Kem", price="10000")
    product = api_client.post(
        "/api/v1/products/",
        {
            "code": "latte",
            "slug": "latte",
            "category": category.id,
            "name": "Latte",
            "topping_ids": [topping.id],
        },
        format="json",
    )
    assert product.status_code == 201
    variant = api_client.post(
        "/api/v1/variants/",
        {
            "product": product.data["id"],
            "code": "latte-m",
            "name": "M",
            "price": "45000.00",
            "is_default": True,
            "no_stock_required": True,
        },
        format="json",
    )
    assert variant.status_code == 201
    detail = api_client.get("/api/v1/menu/latte/")
    assert detail.status_code == 200
    assert detail.data["toppings"][0]["code"] == "test-cream"

    valid = api_client.post(
        "/api/v1/menu/latte/validate-customization/",
        {
            "variant_id": variant.data["id"],
            "topping_ids": [topping.id],
            "sweetness": "70% đường",
            "ice": "50% đá",
            "quantity": 2,
        },
        format="json",
    )
    assert valid.status_code == 200
    assert valid.data["total_price"] == "110000.00"


@pytest.mark.django_db
def test_admin_can_list_toppings_and_upload_product_image(api_client, settings, tmp_path):
    admin = UserFactory(is_superuser=True, is_staff=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    api_client.force_authenticate(admin)
    settings.MEDIA_ROOT = tmp_path
    Topping.objects.create(code="kem-muoi", name="Kem muối", price="10000")

    toppings = api_client.get("/api/v1/toppings/")
    assert toppings.status_code == 200
    assert toppings.data["results"][0]["name"] == "Kem muối"

    image = SimpleUploadedFile(
        "ca-phe.png",
        b"\x89PNG\r\n\x1a\n" + b"demo-image-content",
        content_type="image/png",
    )
    uploaded = api_client.post(
        "/api/v1/products/upload-image/", {"file": image}, format="multipart"
    )

    assert uploaded.status_code == 201
    assert uploaded.data["image_url"].startswith("/media/catalog/products/")
    assert (tmp_path / uploaded.data["image_url"].removeprefix("/media/")).exists()
