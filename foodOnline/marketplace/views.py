from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart
from .context_processors import get_cart_counter,get_cart_ammount
from django.contrib.auth.decorators import login_required

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
    if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user)

    else :
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
       
    }
    return render(request, 'marketplace/vendor_detail.html',context=context)


def add_to_cart(request,food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkcart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    chkcart.quantity +=1
                    chkcart.save()
                    return JsonResponse({'status':'Success','message':'Increased Quantity to cart !','cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'cart_ammount':get_cart_ammount(request)})
                except:
                    chkcart= Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Item saved to cart !','cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'cart_ammount':get_cart_ammount(request)})

            except:
                 return JsonResponse({'status':'Failed','message':'This Food does not exist'})

        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})
        
    else:   
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    


def decrease_cart(request,food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkcart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    if chkcart.quantity > 1:
                        chkcart.quantity -=1
                        chkcart.save()
                    else:
                        chkcart.delete()
                        chkcart.quantity=0
                    return JsonResponse({'status':'Success','cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'cart_ammount':get_cart_ammount(request)})
                except:
                    
                    return JsonResponse({'status':'Failed','message':'you dont have item in your cart'})

            except:
                 return JsonResponse({'status':'Failed','message':'This Food does not exist'})

        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})
        
    else:   
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
@login_required(login_url = 'login')
def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
        cart_count = cart_items.count()
        context = {
            'cart_items': cart_items,
            'cart_count': cart_count,
        }
        return render(request, 'marketplace/cart.html',context=context)
    else:
        return render(request, 'login.html')
    
@login_required(login_url = 'login')
def delete_cart(request,cart_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Item deleted from cart!','cart_counter':get_cart_counter(request),'cart_ammount':get_cart_ammount(request)})
            except:
                 return JsonResponse({'status':'Failed','message':'Cart Item does not exist'})

        else:
            return JsonResponse({'status':'Failed','message':'Invalid request'})
        
    else:   
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    


def search(request):
    if request.method == 'GET':
        address= request.GET.get('address')
        latitude= request.GET.get('lat')
        longitude= request.GET.get('lng')
        radius= request.GET.get('radius')
        keyword = request.GET.get('keyword')

        vendors = Vendor.objects.filter(vendor_name__icontains=keyword,is_approved=True,user__is_active=True)
        vendor_count = vendors.count()

        context ={
            'vendors': vendors,
            'vendor_count': vendor_count,
        }

        return render(request, 'marketplace/listings.html',context=context)
    else:
        return HttpResponse('404 - Not Found')
    

 
