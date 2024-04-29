from django.contrib import admin
from .models import (Products, TopBanner, Promotebanner,
                     Category, Subcategory, ProductSize, CustomerProfile, Cart, OrderPlaced, OrderHistory)


@admin.register(TopBanner)
class TopBannerAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_display = ("description",)
    list_per_page = 50


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 50


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 50


@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 50
