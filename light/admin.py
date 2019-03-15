from django.contrib import admin

from light.models import Light


@admin.register(Light)
class LightAdmin(admin.ModelAdmin):
    list_display = ("room", "is_on", "room_type_command", "last_update")
    list_filter = ("is_on", "room_type_command")
    search_fields = ("room",)
