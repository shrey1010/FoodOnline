from django.urls import path 
from accounts.views import custDashboard
from . import views 

urlpatterns =[
    path('',custDashboard,name="custDashboard"),
    path('profile/',views.cprofile,name="cprofile"),
]