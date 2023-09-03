from django.urls import path,include 
from .views import vprofile
from accounts.views import vendorDashboard

urlpatterns = [
    path("",vendorDashboard,name='vendor'),
    path('profile/',vprofile,name='vprofile'),    
]