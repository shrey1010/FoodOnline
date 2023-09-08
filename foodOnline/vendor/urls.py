from django.urls import path,include 
from .views import vprofile,menuBuilder,fooditems_by_category
from accounts.views import vendorDashboard

urlpatterns = [
    path("",vendorDashboard,name='vendor'),
    path('profile/',vprofile,name='vprofile'),  
    path('menu-builder/',menuBuilder,name='menuBuilder'),  
    path('menu-builder/category/<int:pk>/',fooditems_by_category,name='fooditems_by_category')
]