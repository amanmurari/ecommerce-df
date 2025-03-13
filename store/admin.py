from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Products)
class ProductAdim(admin.ModelAdmin):
    list_display= ['title',"description","category","price","sale_price","stock","status","update_date"]


@admin.register(Category)
class CategoryAdim(admin.ModelAdmin):
    list_display= ['name',"description"]
    ordering=("id",)


@admin.register(Wishlist)
class WishlistAdim(admin.ModelAdmin):
    list_display= ['product',"user","date"]


@admin.register(Cart)
class CartAdim(admin.ModelAdmin):
    list_display= ['product',"user","noi","date"]

@admin.register(Rateing)
class CartAdim(admin.ModelAdmin):
    list_display= ['product',"user","star","review"]


@admin.register(Order)
class ProductAdim(admin.ModelAdmin):
    list_display=["city"]
    