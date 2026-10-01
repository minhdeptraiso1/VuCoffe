from django.db import migrations


LOCAL_PRODUCT_IMAGES = {
    "kt-01": "/images/menu-salted-coffee.png",
    "kt-02": "/images/craft-coffee-cup.jpg",
    "kt-03": "/images/hero-coffee-splash.jpg",
    "kt-04": "/images/craft-coffee-cup.jpg",
    "kt-05": "/images/craft-step-3-extraction.jpg",
    "kt-06": "/images/barista-latte-art.jpg",
    "kt-07": "/images/barista-latte-art.jpg",
    "kt-08": "/images/hero-coffee-splash.jpg",
    "kt-09": "/images/craft-step-1-cherries.jpg",
    "kt-10": "/images/ambiance-patio.jpg",
    "kt-11": "/images/ambiance-counter.jpg",
    "kt-12": "/images/ambiance-workspace.jpg",
    "kt-13": "/images/craft-step-2-roasting.jpg",
    "kt-14": "/images/ambiance-counter.jpg",
    "kt-15": "/images/ambiance-patio.jpg",
}


def use_local_product_images(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    for code, image_url in LOCAL_PRODUCT_IMAGES.items():
        Product.objects.filter(code=code).update(image_url=image_url)


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_seed_demo_catalog"),
    ]

    operations = [
        migrations.RunPython(use_local_product_images, migrations.RunPython.noop),
    ]
