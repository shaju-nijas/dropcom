from django.shortcuts import render,HttpResponse,redirect
from accounts.models import Users
from django.contrib import messages
import random
from PlayAndWin.models import Lottodrop
from datetime import datetime 
from django.utils import timezone
# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        user = Users.objects.get(user = request.user)
        if user.is_active == True:
            context = {
                'user':user,
            }
            if Lottodrop.objects.filter(user = request.user).exists():
                datas = Lottodrop.objects.filter(user = request.user)
                context ['datas'] = datas
            return render(request,'games-page/home.html',context)
        else:
            return redirect('../../accounts/buy-subscription')
    else:
        return redirect('../')
    
def lottodrop(request):
    if request.user.is_authenticated:
        user = Users.objects.get(user = request.user)
        if user.coins >= 50:
            if request.method == "POST":
                num1 = request.POST['num1']
                num2 = request.POST['num2']
                num3 = request.POST['num3']
                num4 = request.POST['num4']
                num5 = request.POST['num5']
                num6 = request.POST['num6']
                numbers_set = set([num1,num2,num3,num4,num5,num6])
                numbers = ','.join(str(x) for x in numbers_set)
                Lottodrop.objects.get_or_create(
                    user = request.user,
                    created_at = datetime.now(),
                    number = numbers
                )
                user.coins -= 50
                user.save()
                return redirect (lottodrop)
            return render(request,'games-page/lottodrop.html',{'user':user})
        else:
            messages.error(request,"minimum 50 coins needed to play lottodrop")
            return redirect(homepage)
    else:
        return redirect('../')
    