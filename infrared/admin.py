from django.contrib import admin

from infrared.models import Infrared


@admin.register(Infrared)
class InfraredAdmin(admin.ModelAdmin):
    list_display = ("room", "position", "human_detected", "last_time_human_detected", "last_update")
    list_filter = ("human_detected", "position")
    search_fields = ("room",)
