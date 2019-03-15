from django.contrib import admin

from room.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("hid", "room_number", "floor", "status")
    list_filter = ("status",)
    search_fields = ("room_number", "hid")
