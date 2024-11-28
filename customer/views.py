from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
def dashboard(request):
    user= User.objects.get(email=request.user.email)
    return render(request, "customer/profile.html")
