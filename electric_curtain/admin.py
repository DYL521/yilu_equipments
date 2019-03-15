from django.contrib import admin

from electric_curtain.models import Curtain

@admin.register(Curtain)
class CurtainAdmin(admin.ModelAdmin):
    list_display = ("room", "room_type_command", "last_update")
    list_filter = ("room_type_command",)
    search_fields = ("room",)
