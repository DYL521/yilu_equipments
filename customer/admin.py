from django.contrib import admin

from customer.models import Order, StayInfo


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("PMS_type", "PMS_ID", "start", "end")
    list_filter = ("PMS_type",)
    search_fields = ("PMS_ID",)


@admin.register(StayInfo)
class StayInfoAdmin(admin.ModelAdmin):
    list_display = ("order", "customer_id", "room")
