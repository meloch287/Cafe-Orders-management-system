from django.contrib import admin
from .models import Order
from .models import MenuItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'total_price', 'status')

admin.site.register(MenuItem)
