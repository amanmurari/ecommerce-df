from django.urls import path
from .views import *
urlpatterns=[
    path("",cart),
    path("delete/",delete_cart),
    path("update/",update_cart),
    path("add/",add_cart),
]