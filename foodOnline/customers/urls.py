from django.urls import path 
from accounts.views import custDashboard
from . import views 

urlpatterns =[
    path('',custDashboard,name="custDashboard"),
    path('profile/',views.cprofile,name="cprofile"),
    path('my_orders/',views.my_orders,name='customer_my_orders'),
    path('order_detail/<int:order_number>/',views.order_detail,name='customer_order_detail'),
]