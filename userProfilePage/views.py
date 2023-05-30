import time
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from accounts.models import User,Users,Subscription
from userHomePage.models import Products,Order,OrderItem,CheckoutAddress,BankAccountDetails,ReturnOrdersBankDetails,ReturnOrdersRefund
from products.models import AffiliateCommission
from userProfilePage.models import Withdraws,ContactUs
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from userProfilePage.forms import ChangePasswordForm
from django.utils import timezone

# Create your views here.

def profile(request):
    if request.user.is_authenticated:
        user = Users.objects.get(user=request.user)
        if BankAccountDetails.objects.filter(user = request.user).exists():
            get_user_bank = BankAccountDetails.objects.get(user = request.user)
            return render(request,'profile-page/profile.html',{'user':user,'bank':get_user_bank})
        return render(request,'profile-page/profile.html',{'user':user})
    else:
        return redirect('/accounts')
    

def userOrders(request):
    user = Users.objects.get(user=request.user)
    get_userOrders = Order.objects.filter(user=request.user,ordered = True).order_by('-start_date')

    context={
        'user':user,
        'orders':get_userOrders
    }
    return render(request,'profile-page/user-orders.html',context)
    
def userOrderDetail(request,id):
    user = Users.objects.get(user=request.user)
    order = get_object_or_404(Order, id=id, user=request.user)
    address = CheckoutAddress.objects.get(user=request.user)
    return render(request,'profile-page/user-order-detail.html',{'order':order,'user':user,'address':address})   

def cancelOrder(request,id):
    user = Users.objects.get(user=request.user)
    get_order = Order.objects.get(id=id)
    if get_order.order_recieved == True:
        return HttpResponse("your order is already shipped..you cant able to cancel your order..!") 
    else:
        get_order.order_cancelled = True
        if get_order.coin_discount != 0:
            user.coins += get_order.coin_discount
        user.wallet += int(get_order.get_total_final_price())
        user.refunded_amount += int(get_order.get_total_final_price())
        user.save()
        get_order.save()
        return redirect(userOrders)     

def referAndEarn(request):
    if request.user.is_authenticated:
        subscribe = Subscription.objects.get(user = request.user)
        if subscribe.payment_status == True:
            user = Users.objects.get(user=request.user,is_active = True)
            return render(request,'profile-page/refer&earn.html',{'user':user})
        else:
            return redirect('../accounts/buy-subscription')
    return redirect('/accounts') 

def userCoins(request):
    if request.user.is_authenticated:
        user = Users.objects.get(user=request.user)
        affiliate_commission_db = AffiliateCommission.objects.filter(user=request.user)
        return render(request,'profile-page/coins-page.html',{'user':user,'coin_dashboard':affiliate_commission_db})
    else:
        return redirect('/accounts')
   

def transferCoins(request):
    get_user = Users.objects.get(user=request.user)
    if get_user.coins >= 999:
        get_user.wallet += get_user.coins
        get_user.coins = 0
        get_user.save()
        messages.success(request,'Coins successfully transferred to wallet..')
        return redirect(userCoins)
    else:
        messages.error(request,'Minimum 999 coins required to transfer to wallet..')
        return redirect(userCoins)

def userWallet(request):
    get_user = Users.objects.get(user = request.user)
    if BankAccountDetails.objects.filter(user = request.user).exists():
        user_bank = BankAccountDetails.objects.get(user=request.user)
        try:
            check_user = Withdraws.objects.get(user=request.user,withdraw_requested = True)
            data = Withdraws.objects.filter(user=request.user).order_by('-id')
            return render(request,'profile-page/wallet.html',{'user':get_user,'check':check_user,'datas':data,'bank':user_bank})
        except:
            pass
        data = Withdraws.objects.filter(user=request.user).order_by('-id')
        return render(request,'profile-page/wallet.html',{'user':get_user,'datas':data,'bank':user_bank})
    return render(request,'profile-page/wallet.html',{'user':get_user,'bank_account':'False'})  

def addBankAcc(request):
    user = Users.objects.get(user=request.user)
    if request.method == "POST":
        account_holder_name = request.POST['account_holder_name']
        account_number = request.POST['account_number']
        IFSC_code = request.POST['IFSC_code']
        bank_name = request.POST['bank_name']
        bank_branch = request.POST['bank_branch']

        userBankDetails = BankAccountDetails(
            user = user.user,
            account_holder_name = account_holder_name,
            account_number = account_number,
            IFSC_code = IFSC_code,
            bank_name = bank_name,
            bank_branch = bank_branch
        )
        userBankDetails.save()
        messages.success(request,"Bank account added successfully")
        return redirect(userWallet)
    return render(request,'profile-page/bank-account.html',{'user':user})  

def editBankAcc(request):
    if request.method == "POST":
        account_holder_name = request.POST['account_holder_name']
        account_number = request.POST['account_number']
        IFSC_code = request.POST['IFSC_code']
        bank_name = request.POST['bank_name']
        bank_branch = request.POST['bank_branch']

        if BankAccountDetails.objects.filter(account_number = account_number).exists():
            return HttpResponse("Account number is already used")
        else:
            BankAccountDetails.objects.filter(user = request.user).update(
                account_holder_name = account_holder_name,
                account_number = account_number,
                IFSC_code = IFSC_code,
                bank_name = bank_name,
                bank_branch = bank_branch
            )
            messages.success(request,"Bank account details edited successfully..")
            return redirect('../profile')
    return render(request,'profile-page/bank-account.html',{'editAccount':'Yes'})

def withdrawRequest(request):
    get_user = Users.objects.get(user = request.user)
    if get_user.is_active == True:
        get_bank = BankAccountDetails.objects.get(user = request.user)
        if request.method == "POST":
            withdraw_requested_amount = request.POST['withdraw_requested_amount']
            req_amount = int(withdraw_requested_amount)
            if 30 <= req_amount <= get_user.wallet:
                reqWithdraw = Withdraws(
                    user = get_user.user,
                    withdraw_requested_amount = req_amount,
                    withdraw_requested = True,
                    withdrawed_amount = 0,
                    withdraw_status = False,
                    date_time_of_withdraw_requested = datetime.now()
                )
                reqWithdraw.save()
                get_user.wallet -= req_amount
                get_user.save()
                get_bank.withdraw_requested = True
                get_bank.save()
                messages.success(request,"Withdraw requested successfully..")
                return redirect(userWallet)
            else:
                messages.error(request,"Withdraw failed")
                return redirect(userWallet)
    else:
        return redirect('../accounts/buy-subscription')         

def contactAdmin(request):
    user = Users.objects.get(user = request.user)
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        ContactUs.objects.create(
            user = request.user,
            name = name,
            email = email,
            subject = subject,
            message = message,
            date = datetime.now()
        )
        messages.success(request,"Thank you for contacting us..Our team will come back to you within a matter of hours to help you..")
        return redirect(contactAdmin)
    return render(request,'profile-page/contact-page.html',{'user':user})

def change_passsword(request,user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.save()
        messages.success(request,'password changed successfully..Login again..')
        return redirect('../')
    else:
        return HttpResponse("505 ERROR OCCURED")

def about_us(request):
    return render(request,'profile-page/about-us.html')

def returnOrderRequest(request,id):
    get_order = Order.objects.get(id=id)
    if get_order.order_delivered == True:
        if ReturnOrdersRefund.objects.filter(user = request.user, return_requested = True).exists():
            messages.error(request,'You cannot return the order at this time. Your previous returned order is already being processed')
            return redirect(userOrders)
        else:
            join_date = get_order.order_expected_delivery_date
            current_date = timezone.now()
            time_difference = current_date - join_date
            if time_difference.days <= 4:
                ReturnOrdersRefund.objects.create(
                    user = request.user,
                    return_Date = datetime.now(),
                    return_Amount = int(get_order.get_total_final_price()),
                    returned_Order = get_order,
                    return_requested = True,
                )
                Order.objects.filter(user=request.user,order_id = get_order.order_id).update(
                    order_return_requested = True
                )
                messages.success(request,"Product ID "+ get_order.order_id +" successfully requested to return")
                return redirect(userOrders)
            else:
                messages.error(request,'You cannot return the order at this time. You are already 4 days after delivery..')
                return redirect(userOrders)  
    else:
        pass
    return redirect(userOrders)    



def returnBankDetails(request,id):
    if ReturnOrdersRefund.objects.filter(user = request.user,return_requested = True,returned_Order = id).exists():
        get_data = ReturnOrdersRefund.objects.get(user = request.user,return_requested = True,returned_Order = id)
        get_order = Order.objects.get(order_id = get_data.returned_Order.order_id,order_return_requested = True)
        print(get_order.returned_order_refund_requested)
        get_order.returned_order_refund_requested = True
        get_order.save()
        print(get_order.returned_order_refund_requested)
        if request.method == "POST":
            acc_holder_name = request.POST['acc_holder_name']
            account_number = request.POST['account_number']
            IFSC_code = request.POST['IFSC_code']
            bank_name = request.POST['Bank_name']
            bank_branch = request.POST['Bank_branch']

            ReturnOrdersBankDetails.objects.create(
                user = request.user,
                acc_holder_name = acc_holder_name,
                acc_num = account_number,
                IFSC_code = IFSC_code,
                bank = bank_name,
                bank_branch = bank_branch,
                withdraw_requested = True,
            )
            messages.success(request,"Your refund request has been successfully completed.. your refund will be processed within 1-4 business days. thank you..")
            return redirect(userOrders) 
    else:
        return HttpResponse('404 ERROR..')