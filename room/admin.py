from django.contrib import admin

from room.models import Room, RoomType, Hotel


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("hid", "room_number", "floor", "status")
    list_filter = ("status",)
    search_fields = ("room_number", "hid")


@admin.register(RoomType)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_type_name", "hotel")

@admin.register(Hotel)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("hid", "bangqi_url", "samsung_ac_url")