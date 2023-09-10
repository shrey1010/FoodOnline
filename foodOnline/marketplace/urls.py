from django.urls import path 
from .import views 

urlpatterns = [
    path('marketplace/',views.marketplace,name = "marketplace")

]