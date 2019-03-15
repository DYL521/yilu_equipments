from django.contrib import admin

from cateye.models import CatEye, CatEyeSoftwareVersion


@admin.register(CatEye)
class CatEyeAdmin(admin.ModelAdmin):
    list_display = ("room", "private_ip", "push_id", "software_version", "hardware_version", "last_seen")
    search_fields = ("room",)
    readonly_fields = ("private_ip", "push_id", "software_version", "hardware_version", "last_seen")


@admin.register(CatEyeSoftwareVersion)
class CatEyeSoftwareVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "size", "apk", "log", "md5")
    list_filter = ("is_active",)
    readonly_fields = ("created", "last_update")
    
