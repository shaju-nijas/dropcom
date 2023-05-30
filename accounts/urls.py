from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.registerPage,name='register_page'),
    path('login',views.loginPage,name='login_page'),
    path('logout',views.user_logout,name='logout'),
    path('buy-subscription',views.subscription,name='subscription'),
    path('payment',views.payment,name='payment'),
    path('handlerequest',views.handlerequest,name='handlerequest'),
    path('addreferals',views.addReferals,name="addreferals"),
]