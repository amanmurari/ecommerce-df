from django.shortcuts import render,redirect
import json
from django.http import JsonResponse

from .models import Products,User,Rateing,Cart
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def home(request):
    products= Products.objects.filter(status="published")
    context={
        "products":products
    }
    return render(request,"store/index.html",context)


def product_details(request,num,name):
    product= Products.objects.get(pk=num,title=name)
    product_list= Products.objects.filter(category=product.category)
    reviews = Rateing.objects.filter(product__id=product.id)
    cart=True
    if request.user.is_authenticated:
        if Cart.objects.filter(product__id=product.id,user__id=request.user.id):
            cart=False

    print(cart)
    context={
        "product":product,
        "product_list":product_list,
        "reviews":reviews,"cart":cart
    }
    return render(request,"store/product.html",context)

def products(request):
    products= Products.objects.filter(status="published")
    context={
        "products":products
    }
    return render(request,"store/products.html",context)


@csrf_exempt
def rate(request):
    if request.method=="POST":
        try:
            data= json.load(request)
            print(data)
            review= data["review"]
            star= data["star"]
            u_id= data["uid"]
            p_id= data["pid"]
            product=Products.objects.get(pk=p_id)
            usr=User.objects.get(username=u_id)
            rate= Rateing(user=usr,product=product,review=review,star=star)
            rate.save()
            return JsonResponse({"status":200})
        except Exception:
            print("post")
            return JsonResponse({"status":404})
        
    else:
        return JsonResponse({"status":404})

        
