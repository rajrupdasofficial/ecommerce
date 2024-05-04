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
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import uuid
import json

# Create your views here.

"""stripe secret key init that stripe can identify which application it's trying to"""
stripe.api_key = settings.STRIPE_SECRET_KEY

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
        cart_product = Cart.objects.filter(
            user=user)  # Filter directly for the user
        total_products = cart_product.count()
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (Decimal(p.quantity) *
                              Decimal(p.product.discount))
                print(type(tempamount))
                amount += Decimal(tempamount)
                totalamount = amount
            return render(request, 'app/addtocart.html', context={'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem': total_products})
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
    amount = Decimal(0.0)
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (Decimal(p.quantity) * Decimal(p.product.discount))
            amount += Decimal(tempamount)
        totalamount = Decimal(amount)
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


"""payment done section"""


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = CustomerProfile.objects.get(user=user)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


"""orders page"""


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', context={'order_placed': op})


"""stripe payment process section"""


# @csrf_exempt
# @login_required
# def payment_process(request):
#     if request.method == 'POST':
#         data_str = request.body  # Convert POST data to dictionary
#         data = json.loads(data_str)
#         payment_method_id = data.get('payment_method_id')
#         total_amount = data.get('totalamount')
#         cust_email = data.get('custdemail')
#         productid = data.get('productid')

#         return_url = 'http://localhost:8000/paymentdone/success'
#         stripe.api_key = settings.STRIPE_SECRET_KEY

#         try:
#             # Create a PaymentIntent on Stripe
#             payment_intent = stripe.PaymentIntent.create(

#                 amount=int(float(total_amount))*100,
#                 currency='inr',  # Change currency to INR
#                 payment_method=payment_method_id,
#                 confirmation_method='manual',
#                 confirm=True,
#                 return_url=return_url,
#             )

#             # Generate a unique order UID
#             order_uid = uuid.uuid4()

#             # Create a new OrderPlaced instance with the generated UID
#             customer_e_profile = CustomerProfile.objects.get(
#                 user=request.user)
#             product = Products.objects.get(uid=productid)
#             order = OrderPlaced.objects.create(
#                 user=request.user,
#                 product=product,
#                 customer=customer_e_profile
#             )

#             # Store the order UID in the session
#             request.session['order_uid'] = str(order_uid)

#             # Update the order with payment method ID and status
#             order.payment_method_id = payment_method_id
#             order.status = 'Paid'  # Change status to Paid after successful payment
#             order.save()
#             # Remove the purchased item from the user's cart
#             cart_item = get_object_or_404(
#                 Cart, user=request.user, product=product)
#             cart_item.delete()

#             # Redirect to success page
#             return JsonResponse({'success': True})

#         except stripe.error.CardError as e:
#             # Display error to the user if payment fails due to card error
#             return JsonResponse({'success': False, 'error': str(e)})
#         except Exception as e:
#             # Handle other exceptions
#             print("############", e)
#             return JsonResponse({'success': False, 'error': 'An error occurred. Please try again.'})

#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})

# "price_data": {
#     "currency": "inr",
#     "unit_amount": int(total_amount)*100,
#     "product_data": {
#         "name": productname,
#         "description": productdescription,
#         "images": [
#             f"{settings.BACKEND_DOMAIN}/{thumnailurl}"
#         ],
#     },
# },
@csrf_exempt
@login_required
def payment_process(request):
    if request.method == 'POST':
        data_str = request.body  # Convert POST data to dictionary
        data = json.loads(data_str)
        payment_method_id = data.get('payment_method_id')
        total_amount = data.get('totalamount')
        cust_email = data.get('custdemail')
        productid = data.get('productid')
        productquantity = data.get('productquantity')
        productuid = Products.objects.get(uid=productid)
        productname = productuid.heading
        productdescription = productuid.desciption
        thumnailurl = productuid.productimage
        return_url = 'http://localhost:8000/paymentdone/success'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            # Create a PaymentIntent on Stripe

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "unit_amount": Decimal(total_amount)*100,
                            "product_data": {
                                "name": productname,
                                "description": productdescription,
                                "images": [
                                    f"{settings.BACKEND_DOMAIN}/{thumnailurl}"
                                ],
                            },
                        },
                        "quantity": productquantity,
                    },
                ],
                metadata={"product_id": productid},
                mode="payment",
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL
            )
            # Generate a unique order UID
            order_uid = uuid.uuid4()

            # Create a new OrderPlaced instance with the generated UID
            customer_e_profile = CustomerProfile.objects.get(
                user=request.user)
            product = Products.objects.get(uid=productid)
            order = OrderPlaced.objects.create(
                user=request.user,
                product=product,
                customer=customer_e_profile
            )

            # Store the order UID in the session
            request.session['order_uid'] = str(order_uid)

            # Update the order with payment method ID and status
            order.payment_method_id = payment_method_id
            order.status = 'Paid'  # Change status to Paid after successful payment
            order.save()
            # Remove the purchased item from the user's cart
            cart_item = get_object_or_404(
                Cart, user=request.user, product=product)
            cart_item.delete()

            # Redirect to success page
            return JsonResponse({'success': True})

        except stripe.error.CardError as e:
            # Display error to the user if payment fails due to card error
            return JsonResponse({'success': False, 'error': str(e)})
        except Exception as e:
            # Handle other exceptions
            print("############", e)
            return JsonResponse({'success': False, 'error': 'An error occurred. Please try again.'})

    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


"""successpage"""


def success(request):
    return render(request, 'app/success.html')
