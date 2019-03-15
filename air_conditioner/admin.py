from django.contrib import admin

from air_conditioner.models import AirConditioner


@admin.register(AirConditioner)
class AirConditionerAdmin(admin.ModelAdmin):
    list_display = ("room", "is_on", "mode", "temperature", "room_temperature", "wind_direction", "wind_speed")
    list_filter = ("is_on", "mode")
    search_fields = ("room",)
