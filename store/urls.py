from django.urls import path
from .views import *

urlpatterns=[
    path("",home,name="home"),
    path("product/<str:name>/<int:num>/",product_details,name="product"),
    path("products/",products,name="products"),
     path("rateing/",rate,name="rate"),
]