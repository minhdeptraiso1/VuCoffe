import pytest

from apps.accounts.roles import ROLE_ADMIN, assign_role
from apps.accounts.tests.factories import UserFactory
from apps.catalog.models import Variant
from apps.inventory.models import Ingredient


@pytest.mark.django_db
def test_unit_conversion_rejects_cycle(api_client):
    admin = UserFactory(is_superuser=True, is_staff=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    api_client.force_authenticate(admin)
    gram = api_client.post(
        "/api/v1/units/", {"code": "unit-a", "name": "Đơn vị A", "symbol": "a"}, format="json"
    ).data
    kilogram = api_client.post(
        "/api/v1/units/", {"code": "unit-b", "name": "Đơn vị B", "symbol": "b"}, format="json"
    ).data
    assert (
        api_client.post(
            "/api/v1/unit-conversions/",
            {"from_unit": kilogram["id"], "to_unit": gram["id"], "factor": "1000"},
            format="json",
        ).status_code
        == 201
    )
    cycle = api_client.post(
        "/api/v1/unit-conversions/",
        {"from_unit": gram["id"], "to_unit": kilogram["id"], "factor": "0.001"},
        format="json",
    )
    assert cycle.status_code == 400
    assert "to_unit" in cycle.data["details"]


@pytest.mark.django_db
def test_recipe_requires_positive_items(api_client):
    admin = UserFactory(is_superuser=True, is_staff=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    api_client.force_authenticate(admin)
    response = api_client.post("/api/v1/recipes/", {"items": []}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_seeded_sellable_variants_have_recipe_or_explicit_no_stock_flag():
    incomplete = Variant.objects.filter(
        is_active=True,
        no_stock_required=False,
        recipes__is_active=True,
    ).distinct()
    expected = Variant.objects.filter(is_active=True, no_stock_required=False)

    assert set(incomplete.values_list("id", flat=True)) == set(
        expected.values_list("id", flat=True)
    )


@pytest.mark.django_db
def test_admin_can_create_recipe_without_sending_effective_date(api_client):
    admin = UserFactory(is_superuser=True, is_staff=True)
    assign_role(user=admin, role=ROLE_ADMIN)
    api_client.force_authenticate(admin)
    variant = Variant.objects.get(code="kt-01-s")
    ingredients = list(Ingredient.objects.filter(code__in=["robusta", "salt-cream"]))

    response = api_client.post(
        "/api/v1/recipes/",
        {
            "variant": variant.id,
            "items": [
                {"ingredient": ingredient.id, "quantity": "25"} for ingredient in ingredients
            ],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["variant"] == variant.id
    assert response.data["version"] == 2
