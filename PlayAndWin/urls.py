from django.urls import path
from PlayAndWin import views
urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("lottodrop",views.lottodrop,name="lottodrop"),
]