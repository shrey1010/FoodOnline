from django.urls import path 
from .views import registerUser,registerVendor,login,logout,dashboard

urlpatterns = [
    path('registerUser/',registerUser, name='registerUser'),
    path('registerVendor/',registerVendor, name='registerVendor'),
    path('login/',login, name='login'),
    path('logout/',logout, name='logout'),
    path('dashboard/',dashboard, name='dashboard'),
]