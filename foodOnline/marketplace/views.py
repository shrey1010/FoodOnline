from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html',context=context)


def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
        )
    )
    # vendor = Vendor.objects.get(vendor_slug=vendor_slug)
    context = {
        'vendor': vendor,
        'categories': categories,
       
    }
    return render(request, 'marketplace/vendor_detail.html',context=context)


def add_to_cart(request,food_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkcart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    chkcart.quantity +=1
                    chkcart.save()
                    return JsonResponse({'status':'Success','message':'Increased Quantity to cart !'})
                except:
                    chkcart= Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Item saved to cart !'})

            except:
                 return JsonResponse({'status':'Failed','message':'This Food does not exist'})

        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})
        
    else:   
        return JsonResponse({'status':'Failed','message':'Please login to continue'})