from .models import Cart ,Tax
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
    tax_total=0
    grand_total=0
    tax_dict = {}
    if request.user.is_authenticated :
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items :
                    fooditem = FoodItem.objects.get(pk=cart_item.fooditem.id)
                    subtotal += (cart_item.quantity * fooditem.price)
                
                get_tax = Tax.objects.filter(is_active=True)
                for tax in get_tax:
                    tax_type = tax.tax_type
                    tax_percentage = tax.tax_percentage
                    tax_amount = round((subtotal * tax_percentage) / 100,2)
                    tax_dict.update({tax_type:{str(tax_percentage) :tax_amount}})

                for key in tax_dict.values():
                    for x in key.values():
                        tax_total += x
                # tax_total = sum(x for key in tax_dict.values() for x in key.values())

                grand_total = subtotal +tax_total
                    
            else:
                subtotal = 0
                tax_total = 0
                grand_total = 0
        except:
            subtotal = 0
            tax_total = 0
            grand_total = 0

    return dict(subtotal=subtotal,tax=tax_total,grand_total=grand_total,tax_dict=tax_dict)





