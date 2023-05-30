from random import randint
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from accounts.models import User,Users,Subscription
from django.contrib.auth import authenticate,login,logout
from userHomePage.views import index
import time

from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_SECRET))

# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            if User.objects.filter(username = username).exists():
                if User.objects.filter(email = email).exists():
                    user = authenticate(username = username,email = email , password = password)
                    if user is not None:
                        login(request,user)
                        return redirect('/')
                    else:
                        print("password eror")
                        messages.error(request,"invalid password")
                else:
                    print('email not')
                    messages.error(request,"Invalid email ")
            else:
                print('username not')   
                messages.error(request,"Invalid username")                   
    return render (request,'accounts-page/login.html') 

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            invited_by = request.POST['referal_code']

            referral_id = randint(11111,9999999999)

            if password == confirm_password:
                if User.objects.filter(username = username).exists():
                    messages.error(request,'Username already exists..!!')
                else:
                    if Users.objects.filter(phone_number = phone_number).exists():
                        messages.error(request,'Phone number already exists..!!')
                    else:
                        if User.objects.filter(email = email).exists():
                            messages.error(request,'Email already exists..!!')
                        else:
                            new_user = User.objects.create_user(username = username , email = email , password = password)
                            new_user.save()
                            user = Users(
                                user = new_user ,
                                phone_number = phone_number,
                                invited_by_id = invited_by,
                                referral_id = referral_id
                            )
                            user.save()
                            payment = Subscription.objects.create(user = user.user,payment_status = False)
                            user_login = authenticate(username = username,email = email,password = password)
                            if user_login is not None:
                                login(request,new_user)
                                return redirect(index)
                            else:
                                messages.error(request,'error occured..!! Try again.')
            else:
                messages.error(request,'password didnt match !!')
    return render (request,'accounts-page/register.html')  

def user_logout(request):
    logout(request)
    return redirect('/accounts')

def subscription(request):
    if request.user.is_authenticated:
        return render(request,'accounts-page/subscription.html')
    else:
        return redirect('/accounts')


def payment(request):
    try:
        payment = Subscription.objects.get(user=request.user , payment_status = False) 
        order_amount = 99
        order_currency = "INR"
        order_reciept = payment.user.username
        notes = {
            'id' : payment.user.id,
            'name' : payment.user.username,
        } 
        razorpay_payment = razorpay_client.order.create(
            dict (
                amount = order_amount * 100,
                currency = order_currency,
                receipt = order_reciept,
                notes = notes,
                payment_capture = "0",
            )
        )
        payment.razorpay_order_id = razorpay_payment["id"]
        payment.save()
        return render(request,"accounts-page/payment.html",{
            'payment' : payment,
            'order_id' : razorpay_payment["id"],
            'orderId' : payment.user.username,
            'final_price' : order_amount,
            'razorpay_merchant_id' : settings.RAZORPAY_ID,
            'callback_url' : "http://"+"127.0.0.1:8000"+"/accounts/handlerequest",
        })
    except Subscription.DoesNotExist:
        return HttpResponse("404 Error")

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try :
            payment_id = request.POST.get("razorpay_payment_id","")
            order_id = request.POST.get("razorpay_order_id","")
            signature = request.POST.get("razorpay_signature","")

            parameter_dict = {
                'razorpay_payment_id':payment_id,
                'razorpay_order_id':order_id,
                'razorpay_signature':signature,
            }
            try:
                payment_db = Subscription.objects.get(razorpay_order_id = order_id)
            except:
                return HttpResponse("404 error ... payment not found error occured")
            payment_db.razorpay_payment_id = payment_id
            payment_db.razorpay_signature = signature
            payment_db.save()

            result = razorpay_client.utility.verify_payment_signature(parameter_dict)

            if result is not None:
                amount = 99
                amount = amount*100
                razorpay_client.payment.capture(payment_id,amount)
              

                payment_db.payment_status = True 
                payment_db.save()
                
                return redirect('addreferals') 
            else:
                payment_db.payment_status = False
                payment_db.save()
                return redirect('payment')
        except:
            return HttpResponse("404 error occured") 

def addReferals(request):
    if request.user.is_authenticated:
        data = Subscription.objects.get(user=request.user)
        if data.payment_status == True:
            print('refer workes')

            user = Users.objects.get(user=request.user)
            user.coins = 99
            user.is_active = True
            user.save()
            try:
                invited_by_id = user.invited_by_id
                level_1_user = Users.objects.filter(referral_id = invited_by_id).get()
                level_1_user.wallet += 30
                level_1_user.total_earnings += 30
                level_1_user.level_1_count += 1
                level_1_user.level_1_earnings += 30
                level_1_user.save()
                if level_1_user.level_1_count == 10:
                    print("reward got")
                    level_1_user.wallet += 100
                    level_1_user.total_earnings += 100
                    level_1_user.save()    
                user.invited_user = level_1_user.user.username
                user.save()
                print("level 1 saved")
            except:
                print("level 1 not get")   
            try:
                level_2_user = Users.objects.filter(referral_id = level_1_user.invited_by_id).get()
                level_2_user.wallet += 20
                level_2_user.total_earnings += 20
                level_2_user.level_2_count += 1
                level_2_user.level_2_earnings += 20
                level_2_user.save()
                print("level 2 saved")
            except:
                print("level 2 not get")
            try:
                level_3_user = Users.objects.filter(referral_id = level_2_user.invited_by_id).get()
                level_3_user.wallet += 10
                level_3_user.total_earnings += 10
                level_3_user.level_3_count += 1
                level_3_user.level_3_earnings += 10
                level_3_user.save()
                print("level 3 saved")
            except:
                print("level 3 not get")
            try:
                level_4_user = Users.objects.filter(referral_id = level_3_user.invited_by_id).get()
                level_4_user.wallet += 5
                level_4_user.total_earnings += 5
                level_4_user.level_4_count += 1
                level_4_user.level_4_earnings += 5
                level_4_user.save()
                print("level 4 saved")
            except:
                print("level 4 not get")
            try:
                level_5_user = Users.objects.filter(referral_id = level_4_user.invited_by_id).get()
                level_5_user.wallet += 5
                level_5_user.total_earnings += 5
                level_5_user.level_5_count += 1
                level_5_user.level_5_earnings += 5
                level_5_user.save()
                print("level 5 saved") 
            except:
                print('level 5 not found')     
            try:
                level_6_user = Users.objects.filter(referral_id = level_5_user.invited_by_id).get()
                level_6_user.wallet += 5
                level_6_user.total_earnings += 5
                level_6_user.level_6_count += 1
                level_6_user.level_6_earnings += 5
                level_6_user.save()
                print("level 6 saved") 
            except:
                print('level 6 not found')     
            try:
                level_7_user = Users.objects.filter(referral_id = level_6_user.invited_by_id).get()
                level_7_user.wallet += 5
                level_7_user.total_earnings += 5
                level_7_user.level_7_count += 1
                level_7_user.level_7_earnings += 5
                level_7_user.save()
                print("level 7 saved") 
            except:
                print('level 7 not found')     
            messages.success(request,'Subscription successfully purchased..')
            return redirect('/') 
        else:
            print('refer 1 err')
            return redirect('/')
    else:
        print('refer 2 err')
        return redirect('/')               