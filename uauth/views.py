from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    user= User.objects.get(username=request.user.username)
    context={
        'detail':user
    }
    return render(request, "uauth/profile.html",context)

def loginu(request):
    if request.user.is_authenticated:    
        return redirect("/")
    else:
        form= LoginFrom()
        if request.method == "POST":
            form= LoginFrom(request.POST)
            if form.is_valid():
                email= form.cleaned_data['email']
                pass1= form.cleaned_data['password']
                try:
                    d= User.objects.get(email=email)
                    data= authenticate(request,email=email,password=pass1)
                    print(data)
                    if data is not None:
                        print(form.is_valid())
                        login(request,data)
                        messages.success(request,"you are successfully logined")
                        url= request.GET.get("next","/")
                        return redirect(url)
                except:
                    messages.error(request,"email and password are not valid")
                   
                messages.error(request,"email and password are not valid")
            return render(request,"uauth/login.html",{"form":form})       
        return render(request,"uauth/login.html",{"form":form})       
        


def ulogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"you are successfully logout")
        return redirect("/account/login")

def signup(request):
    if request.user.is_authenticated:    
        return redirect("/")
    else:
        form= SignUpFrom()
        if request.method == "POST":
            form= SignUpFrom(request.POST)
            if form.is_valid():
                print("True")
                username= form.cleaned_data['username']
                email= form.cleaned_data['email']
                pass2= form.cleaned_data['password2']
                pass1= form.cleaned_data['password1']
                emailex= User.objects.filter(email=email).exists()
                unameex= User.objects.filter(username=username).exists()
                print(bool(emailex) , bool(unameex),(emailex and unameex))
                if (pass1==pass2) and ( not emailex and not unameex) :
                    print("True")
                    user= User(email=email,username=username,password=pass1)
                    user.save()
                    data= authenticate(email=email,password=pass1)
                    login(request,data)
                    return render("/")
                return render(request,"uauth/signup.html",{"form":form})       
                
            return render(request,"uauth/signup.html",{"form":form})       
        return render(request,"uauth/signup.html",{"form":form})
    

