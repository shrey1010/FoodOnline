from django.urls import path,include 
from .views import vprofile,menuBuilder,fooditems_by_category,add_Category,edit_Category,delete_Category
from accounts.views import vendorDashboard

urlpatterns = [
    path("",vendorDashboard,name='vendor'),
    path('profile/',vprofile,name='vprofile'),  
    path('menu-builder/',menuBuilder,name='menuBuilder'),  
    path('menu-builder/category/<int:pk>/',fooditems_by_category,name='fooditems_by_category'),

    # category crud
    path('menuBuilder/category/add/',add_Category,name='add_category'),
    path('menuBuilder/category/edit/<int:pk>/',edit_Category,name='edit_category'),
    path('menuBuilder/category/delete/<int:pk>/',delete_Category,name='delete_category'),
]