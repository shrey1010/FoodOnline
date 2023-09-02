from django.contrib import admin
from .models import Vendor 
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ("User","vendor_name","is_approved","created_at")
    list_display_links = ("User","vendor_name")

admin.site.register(Vendor, VendorAdmin)
