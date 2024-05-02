from django.contrib import admin
from .models import (Products, TopBanner, Promotebanner,
                     Category, Subcategory, ProductSize, CustomerProfile, Cart, OrderPlaced, OrderHistory, Sliders, ThreeCards)


@admin.register(ThreeCards)
class ThreeCarsConrollerAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 20


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 10


@admin.register(OrderPlaced)
class OrderPlaceAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 10


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 10


@admin.register(CustomerProfile)
class CustomerProfilePage(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 10


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 10


@admin.register(Promotebanner)
class PromoteBannerAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 10


@admin.register(Sliders)
class SliderAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 10


@admin.register(TopBanner)
class TopBannerAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_display = ("description",)
    list_per_page = 50


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    exclude = ["uid", "slug",]
    list_per_page = 50


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 50


@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    exclude = ["uid",]
    list_per_page = 50
