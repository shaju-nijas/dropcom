from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from accounts.models import Subscription,Users

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin-page/')
        else:
            return redirect('/user-home-page')
    else:
        return redirect('/accounts')

def home(request):
    if request.user.is_authenticated:
        user = Users.objects.get(user=request.user)
        categories = Categories.objects.all()
        carousel = CarouselImages.objects.all()
        return render(request,'user-home/index.html',{'categories':categories,'carousel':carousel,'user':user})
    else:
        return redirect('/accounts')


def products(request,id):
    if request.user.is_authenticated:
        user = Users.objects.get(user=request.user)
        products = Products.objects.filter(category = id)
        return render(request,'user-home/products-list.html',{'products':products,'user':user})
    else:
        return redirect('/accounts')
 
  
def product_details(request,id):
    if request.user.is_authenticated:
        user = Users.objects.get(user=request.user)
        product = Products.objects.get(id=id) 
        return render(request,'user-home/product-details.html',{'product':product,'user':user}) 
    else:
        return redirect('/accounts')


  

