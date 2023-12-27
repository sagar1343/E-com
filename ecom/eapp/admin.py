from django.contrib import admin

from .models import Product, Category, CartItem


# Register your models here.


class ProductList(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


admin.site.register(Product, ProductList)
admin.site.register([Category, CartItem])
