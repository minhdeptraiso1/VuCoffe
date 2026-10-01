from django.db import migrations
from django.utils.text import slugify


CATEGORIES = [
    ("traditional", "Cà phê truyền thống"),
    ("modern", "Espresso & Latte"),
    ("coldbrew", "Cold Brew ủ lạnh"),
    ("tea", "Trà & Giải nhiệt"),
    ("pastry", "Bánh ngọt điểm tâm"),
]

PRODUCTS = [
    ("kt-01", "Cà phê Muối Kim Thành", "traditional", 35000, "Cốt Robusta đậm hòa cùng lớp kem muối biển mềm mịn.", "/images/menu-salted-coffee.png", True, True),
    ("kt-02", "Cà phê Trứng Hanoian", "traditional", 42000, "Kem trứng sánh mịn trên nền cà phê phin thơm nồng.", "https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&w=1200&q=85", False, True),
    ("kt-03", "Bạc Xỉu Cốt Dừa 3 Tầng", "traditional", 38000, "Sữa đặc, cốt dừa Bến Tre và cà phê phin hài hòa.", "https://images.unsplash.com/photo-1572442388796-11668ba67e53?auto=format&fit=crop&w=1200&q=85", False, True),
    ("kt-04", "Cà Phê Sữa Đá Sài Gòn", "traditional", 32000, "Robusta pha phin cùng sữa đặc và đá lạnh.", "/images/craft-coffee-cup.jpg", False, True),
    ("kt-05", "Cà Phê Đen Phin Đậm Vị", "traditional", 29000, "Robusta rang mộc, vị đắng đậm và hậu ngọt sâu.", "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=1200&q=85", False, False),
    ("kt-06", "Caramel Macchiato Hạt Dẻ", "modern", 46000, "Espresso kép, sữa tươi và sốt caramel vani.", "/images/barista-latte-art.jpg", True, False),
    ("kt-07", "Cappuccino Bột Quế Thơm", "modern", 42000, "Espresso, sữa nóng và bọt sữa rắc bột quế.", "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=1200&q=85", False, False),
    ("kt-08", "Cold Brew Cam Quế Thảo Mộc", "coldbrew", 45000, "Arabica ủ lạnh 18 giờ cùng cam vàng và quế.", "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=1200&q=85", True, True),
    ("kt-09", "Cold Brew Chanh Vàng Mật Ong", "coldbrew", 45000, "Chanh vàng và mật ong trên nền cà phê ủ lạnh.", "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=1200&q=85", False, False),
    ("kt-10", "Trà Oolong Đào Dâu Tằm", "tea", 39000, "Oolong Bảo Lộc, đào giòn và mứt dâu tằm.", "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=1200&q=85", True, True),
    ("kt-11", "Trà Mãng Cầu Xiêm Tươi", "tea", 42000, "Mãng cầu tươi dầm hòa cùng trà lài thanh khiết.", "https://images.unsplash.com/photo-1497534446932-c925b458314e?auto=format&fit=crop&w=1200&q=85", False, False),
    ("kt-12", "Matcha Latte Kem Phô Mai", "tea", 45000, "Matcha Uji, sữa tươi và kem phô mai mằn mặn.", "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=1200&q=85", False, False),
    ("kt-13", "Croissant Bơ Pháp Nướng Giòn", "pastry", 32000, "Bánh nghìn lớp thơm bơ, vỏ giòn và ruột xốp mềm.", "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=1200&q=85", True, True),
    ("kt-14", "Bánh Tiramisu Cà Phê Espresso", "pastry", 45000, "Ladyfinger thấm espresso cùng kem Mascarpone.", "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=1200&q=85", False, False),
    ("kt-15", "Bánh Mousse Chanh Leo", "pastry", 38000, "Mousse chanh leo chua ngọt nhẹ và mềm mịn.", "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=1200&q=85", False, False),
]


def seed_catalog(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Product = apps.get_model("catalog", "Product")
    Variant = apps.get_model("catalog", "Variant")
    Topping = apps.get_model("catalog", "Topping")
    ProductTopping = apps.get_model("catalog", "ProductTopping")
    categories = {}
    for order, (code, name) in enumerate(CATEGORIES, start=1):
        categories[code], _ = Category.objects.update_or_create(
            code=code, defaults={"name": name, "display_order": order, "is_active": True}
        )
    toppings = []
    for code, name, price in [
        ("salt-cream", "Kem muối biển", 10000),
        ("egg-cream", "Kem trứng", 12000),
        ("coffee-jelly", "Thạch cà phê", 8000),
        ("pearl", "Trân châu trắng", 8000),
    ]:
        topping, _ = Topping.objects.update_or_create(
            code=code,
            defaults={"name": name, "price": price, "is_active": True, "no_stock_required": True},
        )
        toppings.append(topping)
    for order, (code, name, category, price, description, image, featured, best) in enumerate(PRODUCTS, start=1):
        product, _ = Product.objects.update_or_create(
            code=code,
            defaults={
                "slug": slugify(name),
                "category": categories[category],
                "name": name,
                "description": description,
                "image_url": image,
                "image_position": "center 48%",
                "is_featured": featured,
                "is_best_seller": best,
                "display_order": order,
                "is_active": True,
            },
        )
        for size_order, (size, extra, volume) in enumerate([("S", 0, 350), ("M", 6000, 500), ("L", 10000, 700)]):
            if category == "pastry" and size != "S":
                continue
            Variant.objects.update_or_create(
                code=f"{code}-{size.lower()}",
                defaults={
                    "product": product,
                    "name": "Mặc định" if category == "pastry" else size,
                    "volume_ml": None if category == "pastry" else volume,
                    "price": price + extra,
                    "display_order": size_order,
                    "is_default": size == "S",
                    "is_active": True,
                    "no_stock_required": code != "kt-01",
                },
            )
        if category != "pastry":
            for topping in toppings:
                ProductTopping.objects.get_or_create(product=product, topping=topping)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]
    operations = [migrations.RunPython(seed_catalog, migrations.RunPython.noop)]

