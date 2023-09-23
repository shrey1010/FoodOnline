from django.shortcuts import render,redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_counter,get_cart_ammount
from .forms import OrderForm
from .models import Order,Payment
import simplejson as json
from .utils import genrate_order_number
from django.http import HttpResponse

# Create your views here.

def place_order(request):

    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect("marketplace")
    
    subtotal = get_cart_ammount(request)['subtotal']
    total_tax = get_cart_ammount(request)['tax']
    grand_total = get_cart_ammount(request)['grand_total']  
    tax_data = get_cart_ammount(request)['tax_dict']

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order=Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment-method']
            order.save() #order.id is genrated
            order.order_number = genrate_order_number(order.id)
            order.save()

            context = {
                'order': order,
                'cart_items': cart_items,
            }
            
            return render(request, 'orders/place_order.html',context=context)
        else:
            print(form.errors)
        
    return render(request,'orders/place_order.html')


def payments(request):
    # check ajax request

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
    # store payment details  
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user = request.user,order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

        # update order 
        order.payment = payment
        order.is_ordered = True
        order.save()

        # mpve cart item to ordered food 

        # send order confirmation mail 

        # send order recieve to vender 

        # clear cart 

        # return back to ajax 

    return HttpResponse('payments')