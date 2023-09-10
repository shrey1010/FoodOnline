from django.urls import path 
from .import views 

urlpatterns = [
    path('marketplace/',views.marketplace,name = "marketplace"),
    path('<slug:vendor_slug>/',views.vendor_detail,name = 'vendor_detail'),
    # path('vendor_list/',views.vendor_list,name = 'vendor_list'),
]