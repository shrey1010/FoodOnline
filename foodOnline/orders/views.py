from django.shortcuts import render,redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_counter,get_cart_ammount
from .forms import OrderForm
from .models import Order,Payment,OrderedFood
import simplejson as json
from .utils import genrate_order_number,order_total_by_vendor
from django.http import HttpResponse
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import razorpay
from menu.models import FoodItem
from foodOnline.settings import RAZORPAY_CLIENT_ID,RAZORPAY_CLIENT_SECRET
from marketplace.models import Tax
from django.contrib.sites.shortcuts import get_current_site



client = razorpay.Client(auth=(RAZORPAY_CLIENT_ID, RAZORPAY_CLIENT_SECRET))

# Create your views here.

@login_required(login_url='login')
def place_order(request):

    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect("marketplace")
    
    subtotal = 0
    k={}
    venodors_ids = []
    total_data={}
    get_tax = Tax.objects.filter(is_active=True)
    for i in cart_items:
        if i.fooditem.vendor_id not in venodors_ids:
            venodors_ids.append(i.fooditem.vendor_id)

    for i in cart_items:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id,vendor_id__in=venodors_ids)
        v_id = fooditem.vendor.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price*i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (fooditem.price*i.quantity)
            k[v_id] = subtotal

        # calculate tax DATA
        tax_dict = {}
        for tax in get_tax:
            tax_type = tax.tax_type
            tax_percentage = tax.tax_percentage
            tax_amount = round((subtotal * tax_percentage) / 100,2)
            tax_dict.update({tax_type:{str(tax_percentage) :str(tax_amount)}})

        total_data.update({fooditem.vendor.id:{str(subtotal):str(tax_dict)}})

    
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
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment-method']
            order.save() #order.id is genrated
            order.order_number = genrate_order_number(order.id)
            order.vendors.add(*venodors_ids)
            order.save()

            DATA = {
                "amount": float(grand_total)*100,
                "currency": "INR",
                "receipt": "receipt#"+order.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                }
            }
            rzo_order = client.order.create(data=DATA)
            rzp_order_id = rzo_order['id']

            context = {
                'order': order,
                'cart_items': cart_items,
                'rzp_order_id': rzp_order_id,
                'RZP_KEY_ID':RAZORPAY_CLIENT_ID,
                'rzp_amount': float(grand_total)*100,
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

        ordered_food = OrderedFood.objects.filter(order=order)
        customer_subtotal = 0
        for item in ordered_food:
            customer_subtotal += (item.price * item.quantity)

        tax_data = json.loads(order.tax_data)

        context = {
            'user':request.user,
            'order':order,
            'to_email':order.email,
            'ordered_food':ordered_food,
            'domain':get_current_site(request).domain,
            'customer_subtotal':customer_subtotal,
            'tax_data':tax_data 
        }
        send_notification(mail_subject=mail_subject,mail_template=mail_template,context=context)
        

        # send order recieve to vender 
        mail_subject = 'Order Received'
        mail_template = 'orders/mail_templates/order_received.html'
        to_email =[]
        for item in cart_items:
            if item.fooditem.vendor.user.email not in to_email:
                to_email.append(item.fooditem.vendor.user.email)
                ordered_food_to_vendor = OrderedFood.objects.filter(order=order , fooditem__vendor=item.fooditem.vendor)

                context = {
                    'order':order,
                    'to_email': item.fooditem.vendor.user.email,
                    'ordered_food_to_vendor':ordered_food_to_vendor,
                    'vendor_subtotal':order_total_by_vendor(order,item.fooditem.vendor.id)['subtotal'],
                    'tax_data': order_total_by_vendor(order,item.fooditem.vendor.id)['tax_dict'],
                    'vendor_grand_total':order_total_by_vendor(order,item.fooditem.vendor.id)['grand_total']
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
    






    
