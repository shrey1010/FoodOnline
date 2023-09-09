from django.urls import path,include 
from .views import vprofile,menuBuilder,fooditems_by_category,add_Category,edit_Category,delete_Category,add_Food,edit_Food,delete_Food
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

    # fooditem crud
    path('menuBuilder/food/add/',add_Food,name='add_food'),
    path('menuBuilder/food/edit/<int:pk>/',edit_Food,name='edit_food'),
    path('menuBuilder/food/delete/<int:pk>/',delete_Food,name='delete_food'),
]