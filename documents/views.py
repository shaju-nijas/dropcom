from django.shortcuts import render

# Create your views here.

def privacy_policy(request):
    return render(request,'documents-page/privacy-policy.html')

def termsAndConditions(request):
    return render(request,'documents-page/terms-cond.html')

def cancellationAndRefund(request):
    return render(request,'documents-page/cancellation.html')