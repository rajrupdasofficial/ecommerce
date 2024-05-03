from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import (Products, TopBanner, Promotebanner,
                     Category, Subcategory, ProductSize, CustomerProfile, Cart, OrderPlaced, OrderHistory, Sliders, ThreeCards)
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.http.response import JsonResponse
from decimal import Decimal
# Create your views here.

default_core_cache_set_time = 60  # 1 minutes

"""rendering logic for indexpage"""


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


"""rendering logic for product details page"""


def renderproductdetailspage(request, slug):
    productsdetails = cache.get("productsdetails")
    if productsdetails is None:
        productsdetails = get_object_or_404(Products,  slug=slug)
        cache.set("productdetails", productsdetails,
                  default_core_cache_set_time)
    context = {
        "product": productsdetails
    }
    return render(request, "app/productdetails.html", context)


"""rendering logic for cart"""


@login_required
def add_to_cart(request):
    user = request.user
    print(user)
    productid = request.GET.get('prod_id')
    product = Products.objects.get(uid=productid)
    Cart(user=user, product=product).save()
    return redirect('/cart')


"""rendering logic for show cart"""


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = Decimal(0.0)
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount)
                print(type(tempamount))
                amount += Decimal(tempamount)
                totalamount = amount
            return render(request, 'app/addtocart.html', context={'carts': cart, 'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')


"""add to cart extra logics"""

"""plus cart logic"""


def plus_cart(request):
    try:
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product__uid=prod_id)
                                 & Q(user=request.user))
            c.quantity += 1
            c.save()
            amount = Decimal(0.0)
            cart_product = [
                p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = (Decimal(p.quantity) * Decimal(p.product.pricing))
                amount += Decimal(tempamount)
                # totalamount=amount+shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount,
            }
            return JsonResponse(data)
    except Exception as e:
        print("#"*10, e)
        # return JsonResponse(data)


"""minus cart logic"""


def minus_cart(request):
    try:
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product__uid=prod_id)
                                 & Q(user=request.user))
            c.quantity -= 1
            c.save()
            amount = Decimal(0.0)
            cart_product = [
                p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount)
                amount += Decimal(tempamount)
                # totalamount=amount+shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount,
            }
            return JsonResponse(data)
    except Exception as e:
        print("#"*10, e)
        # return JsonResponse(data)


"""remove cart logic"""


def remove_cart(request):
    try:
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product__uid=prod_id)
                                 & Q(user=request.user))

            c.delete()
            amount = Decimal(0.0)
            cart_product = [
                p for p in Cart.objects.all() if p.user == request.user]
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount)
                amount += Decimal((tempamount))
                # totalamount=amount

            data = {
                'amount': amount,
                'totalamount': amount,
            }
            return JsonResponse(data)
    except Exception as e:
        print("#"*10, e)

        # return JsonResponse(data)
"""checkout process"""


@ login_required
def checkout(request):
    user = request.user
    add = CustomerProfile.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount)
            amount += tempamount
        totalamount = amount
    return render(request, 'app/checkout.html', context={'add': add, 'totalamount': totalamount, 'cart_items': cart_items})


"""customer reistration view"""


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'app/registration.html', context)

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Registered Successfully")
            form.save()
        return render(request, 'app/registration.html', context={'form': form})


"""Logout view"""


def logout_view(request):
    logout(request)
    return redirect('login')


"""profile view"""


@ method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()

        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            phonenumber = form.cleaned_data['phonenumber']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = CustomerProfile(
                user=usr, name=name, phonenumber=phonenumber, locality=locality, city=city, zipcode=zipcode, state=state)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')

        return render(request, 'app/profile.html', context={'form': form, 'active': 'btn-primary'})


"""customer address views"""


@ login_required
def address(request):
    add = CustomerProfile.objects.filter(user=request.user)
    return render(request, 'app/address.html', context={'add': add, 'active': 'btn-primary'})
