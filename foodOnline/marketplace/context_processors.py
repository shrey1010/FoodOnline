from .models import Cart 
from menu.models import FoodItem


def get_cart_counter(request) :
    cart_count =0
    if request.user.is_authenticated :
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items :
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count =0

    return dict(cart_count=cart_count)


def get_cart_ammount(request):
    subtotal=0
    tax=0
    grand_total=0
    if request.user.is_authenticated :
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items :
                    fooditem = FoodItem.objects.get(pk=cart_item.fooditem.id)
                    subtotal += (cart_item.quantity * fooditem.price)
                    tax = (subtotal * 18)/100
                    grand_total = subtotal + tax
            else:
                subtotal = 0
                tax = 0
                grand_total = 0
        except:
            subtotal = 0
            tax = 0
            grand_total = 0

    return dict(subtotal=subtotal,tax=tax,grand_total=grand_total)





