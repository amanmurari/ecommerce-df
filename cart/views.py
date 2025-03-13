import json
from django.db.models import Sum,Avg
from django.shortcuts import render,redirect
from django.http import JsonResponse
from store.models import Products,User,Cart,Order
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth.decorators import login_required
@csrf_exempt
def add_cart(request):
    if request.method=="POST":
        try:
            data= json.load(request)
           
            noi= data["noi"]
            u_id= data["uid"]
            p_id= data["pid"]
            product=Products.objects.get(pk=p_id)
            usr=User.objects.get(username=u_id)
            rate= Cart(user=usr,product=product,noi=noi)
            rate.save()
            return JsonResponse({"status":200,"message":True})
        except Exception:
            print("post")
            return JsonResponse({"status":404,"message":False})
        
    else:
        return JsonResponse({"status":404,"message":False})
    



@csrf_exempt
def update_cart(request):
    if request.method=="POST":
        try:
            data= json.load(request)
            
            ids= data["ids"]
            noi= data["noi"]
            u_id= data["uid"]
            p_id= data["pid"]
            product=Products.objects.get(pk=p_id)
            usr=User.objects.get(username=u_id)
            rate= Cart(id=ids,user=usr,product=product,noi=noi)
            rate.save()
            carts= Cart.objects.filter(user__username=request.user.username)
            total=0
            for i in carts:
                if i.product.sale_price is not None:
                    total+=(i.product.sale_price*i.noi)
                else:
                    total+=(i.product.price*i.noi)
            return JsonResponse({"status":200,"price": (rate.product.price*rate.noi),"total":total})
        except Exception:
            print("post")
            return JsonResponse({"status":404})
        
    else:
        return JsonResponse({"status":404})


@csrf_exempt
def delete_cart(request):
    if request.method=="POST":
        try:
            data= json.load(request)
            
            ids= data["ids"]
            
            rate= Cart(pk=ids)
            rate.delete()
            print("delete")
            return JsonResponse({"status":200})
        except Exception:
            print("post")
            return JsonResponse({"status":404})
        
    else:
        return JsonResponse({"status":404})


@login_required
def cart(request):
    if request.user.is_authenticated:
        carts= Cart.objects.filter(user__username=request.user.username)
        total=0
        for i in carts:
            if i.product.sale_price is not None:
                total+=(i.product.sale_price*i.noi)
            else:
                total+=(i.product.price*i.noi)
                
        context={"carts":carts,
                 "total":total}
        print(total)
        return render(request,"cart/cart.html",context)
    else:
        return redirect("/account/login")
   

   
@login_required
def checkout(request):
    carts= Cart.objects.filter(user__username=request.user.username)
    total=0
    for i in carts:
        if i.product.sale_price is not None:
            total+=(i.product.sale_price*i.noi)
        else:
            total+=(i.product.price*i.noi)
    context={"carts":carts,"total":total}
    return render(request, "cart/checkout.html",context)

@csrf_exempt
def address(request):
    if request.method=="POST":
        try:
            data= json.load(request)
           
            fn= data["fn"]
            u_id= data["uid"]
            country= data["country"]
            state= data["state"]
            city= data["city"]
            mob= data["mob"]
            adss=data["adss"]
            usr=User.objects.get(username=u_id)
            rate= Order(user=usr,country=country,state=state,city=city,street=adss)
            rate.save()
            return JsonResponse({"status":200,"message":True})
        except Exception:
            print("post")
            return JsonResponse({"status":404})