from django.contrib import admin

from atomization_glass.models import Glass

@admin.register(Glass)
class GlassAdmin(admin.ModelAdmin):
    list_display = ("room", "room_type_command", "last_update")
    list_filter = ("room_type_command",)
    search_fields = ("room",)
