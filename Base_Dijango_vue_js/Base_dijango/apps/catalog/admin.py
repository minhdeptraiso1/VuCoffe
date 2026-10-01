from django.contrib import admin

from .models import Category, PriceHistory, Product, ProductTopping, Topping, Variant

admin.site.register([Category, Product, Variant, Topping, ProductTopping, PriceHistory])
