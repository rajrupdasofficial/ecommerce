from django.urls import path
from .views import index, renderproductdetailspage


urlpatterns = [
    path("", index, name='index'),
    path("<str:slug>/", renderproductdetailspage, name="detailview"),
]
