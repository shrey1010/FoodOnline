import datetime
from vendor.models import Vendor
import simplejson as json 

def genrate_order_number(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    order_number = current_datetime +str(pk)
    return order_number

def order_total_by_vendor(order,vendor_id):
    # vendor = Vendor.objects.get(user=vendor)
    subtotal = 0
    tax = 0 
    tax_dict ={}
    if order.total_data:
        total_data = json.loads(order.total_data)
        data = total_data.get(str(vendor_id))

           
        for key,value in data.items():
            subtotal+=float(key)
            val = value.replace("'",'"')
            val = json.loads(val)
            tax_dict.update(val)
                
            for i in val:
                for j in val[i]:
                    tax+=float(val[i][j])

    grand_total = float(subtotal)+float(tax)
    context={
        'subtotal':subtotal,
        'tax':tax,
        'tax_dict':tax_dict,
        'grand_total':grand_total,
    }


    return context

