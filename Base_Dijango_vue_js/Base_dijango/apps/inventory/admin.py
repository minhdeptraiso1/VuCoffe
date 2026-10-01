from django.contrib import admin

from .models import Ingredient, Recipe, RecipeItem, Supplier, Unit, UnitConversion

admin.site.register([Unit, UnitConversion, Ingredient, Supplier, Recipe, RecipeItem])
