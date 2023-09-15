from django.contrib import admin
from .models import Cart
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','fooditem','quantity','created_at')
    list_filter = ('user','fooditem','quantity')
    search_fields = ('user','fooditem','quantity')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ('created_at','modified_at')
    


admin.site.register(Cart,CartAdmin)