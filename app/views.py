from django.shortcuts import render
from .models import (Products, TopBanner, Promotebanner,
                     Category, Subcategory, ProductSize, CustomerProfile, Cart, OrderPlaced, OrderHistory, Sliders, ThreeCards)
from django.core.cache import cache

# Create your views here.

default_core_cache_set_time = 60  # 1 minutes


def index(request):
    """top banner logic area with caching enabled"""
    topbanner = cache.get('topbanner')
    if topbanner is None:
        topbanner = TopBanner.objects.first()
        # Cache for 1 minutes
        cache.set('topbanner', topbanner, default_core_cache_set_time)
    """category area with caching enabled"""
    category = cache.get('category')
    if category is None:
        category = Category.objects.order_by('-created')[:6]
        cache.set('latest_categories', category, default_core_cache_set_time)
    """Three infomatics card are with caching enabled"""
    threecards = cache.get("threecards")
    if threecards is None:
        threecards = ThreeCards.objects.order_by('-created')[:3]
        cache.set("threecards", threecards, default_core_cache_set_time)
    """Ads banner"""
    promotebanner = cache.get("promotebanner")
    if promotebanner is None:
        promotebanner = Promotebanner.objects.order_by('-created')[:2]
        cache.set("promotebanner", promotebanner, default_core_cache_set_time)
    """products showcase"""
    products = cache.get("products")
    if products is None:
        products = Products.objects.order_by('-created')[:40]
        cache.set("products", products, default_core_cache_set_time)
    context = {"topbanner": topbanner,
               "category": category, "threecards": threecards, "promotebanner": promotebanner, "products": products}
    return render(request, 'app/index.html', context)
