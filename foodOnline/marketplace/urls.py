from django.urls import path 
from .import views 

urlpatterns = [
    path('marketplace/',views.marketplace,name = "marketplace"),    
    path('<slug:vendor_slug>/',views.vendor_detail,name = 'vendor_detail'),
    # path('vendor_list/',views.vendor_list,name = 'vendor_list'),

    # add to cart
    path('add_to_cart/<int:food_id>/',views.add_to_cart,name = 'add_to_cart'),
    path('decrease_cart/<int:food_id>/',views.decrease_cart,name = 'decrease_cart'),
    path('delete_cart/<int:cart_id>/',views.delete_cart,name = 'delete_cart'),
    
]