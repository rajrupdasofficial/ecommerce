from django.urls import path
from .views import index, renderproductdetailspage, CustomerRegistrationView, logout_view
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path("", index, name='index'),
    path("<str:slug>/", renderproductdetailspage, name="detailview"),
    path("accounts/registration/", CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm), name='login'),
    path('accounts/logout/', logout_view, name='logout')
]
