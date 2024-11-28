from django.urls import path
from .views import *
urlpatterns=[
     path("",dashboard,name="dashboard"),
    path("login/",loginu,name="login"),
    path("logout/",ulogout,name="logout"),
    path("signup/",signup,name="signup"),
]