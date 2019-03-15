from django.contrib import admin

from door.models import Door, DoorSensor, Lock


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    list_display = ("room", "is_opened", "open_direction", "last_update")
    list_filter = ("is_opened",)
    search_fields = ("room",)


@admin.register(Lock)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("room", "is_opened", "last_update")
    list_filter = ("is_opened",)
    search_fields = ("room",)


@admin.register(DoorSensor)
class DoorSensorAdmin(admin.ModelAdmin):
    list_display = ("room", "is_opened", "last_update")
    list_filter = ("is_opened",)
    search_fields = ("room",)
