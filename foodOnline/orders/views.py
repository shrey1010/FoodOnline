from django.shortcuts import render,redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_counter,get_cart_ammount
from .forms import OrderForm
from .models import Order,Payment,OrderedFood
import simplejson as json
from .utils import genrate_order_number
from django.http import HttpResponse
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

@login_required(login_url='login')
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

@login_required(login_url='login')
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
        cart_items =Cart.objects.filter(user=request.user).order_by('created_at')
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price *item.quantity
            ordered_food.save()

        

        # send order confirmation mail 
        mail_subject = 'Order Confirmation'
        mail_template = 'orders/mail_templates/order_confirmation.html'
        context = {
            'user':request.user,
            'order':order,
            'to_email':order.email,
        }
        send_notification(mail_subject=mail_subject,mail_template=mail_template,context=context)
        

        # send order recieve to vender 
        mail_subject = 'Order Received'
        mail_template = 'orders/mail_templates/order_received.html'
        to_email =[]
        for item in cart_items:
            if item.fooditem.vendor.user.email not in to_email:
                to_email.append(item.fooditem.vendor.user.email)
        context = {
            'order':order,
            'to_email': to_email,
        }
        send_notification(mail_subject=mail_subject,mail_template=mail_template,context=context)

        
        # clear cart 
        cart_items.delete()
        # return back to ajax 
        response={
            'order_number':order_number,
            'transaction_id':transaction_id,
            'message':'Order Confirmed!'

        }
        return JsonResponse(response)
        

    return HttpResponse('Invalid request')


def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    try:

        order = Order.objects.get(order_number=order_number,payment__transaction_id=transaction_id,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)

        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)

        tax_dict = json.loads(order.tax_data)

        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_dict':tax_dict,
        }
        return render(request,'orders/order_complete.html',context=context)
    except:
        return redirect('home')

    
