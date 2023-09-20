from django.contrib import admin
from .models import Vendor ,OpeningHour
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ("user","vendor_name","is_approved","created_at")
    list_display_links = ("user","vendor_name")
    list_editable = ("is_approved",)

class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ("vendor","day","from_hour","to_hour","is_closed")
    list_display_links = ("vendor","day")
    list_editable = ("from_hour","to_hour")
    list_filter = ("vendor",)
    search_fields = ("vendor__vendor_name","day")
    list_per_page = 25
    ordering = ("vendor","day")
    
admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHoursAdmin)
