from django.urls import path
from .views import checkout, index,  payment_process, renderproductdetailspage, CustomerRegistrationView, logout_view, ProfileView, address, add_to_cart, show_cart, plus_cart, minus_cart, remove_cart, orders, success
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path("", index, name='index'),

    path("accounts/registration/", CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('users/profile/', ProfileView.as_view(), name='profile'),
    path('user/address/', address, name='address'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', show_cart, name='showcart'),
    path('pluscart/', plus_cart),

    path('minuscart/', minus_cart),

    path('removecart/', remove_cart),
    path('checkout/', checkout, name='checkout'),
    path('orders/', orders, name='orders'),

    #     path('paymentdone/', payment_done, name='paymentdone'),
    path('paymentprocess/', payment_process, name='paymentprocess'),
    path('paymentdone/success', success, name='success'),

    # dynamic urls
    path("<str:slug>/", renderproductdetailspage, name="detailview"),
]
