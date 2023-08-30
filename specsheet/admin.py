from django.contrib import admin
from django import forms
from django.db import models

from .models import RefurbishedItem
from .forms import RefurbishedItemForm

class RefurbishedItemAdmin(admin.ModelAdmin):
    form = RefurbishedItemForm
    fieldsets = [
            ("Overview", {"fields": ["date", "builder", "make", "item_model", "serial_no"]}),
            ("Operating system", {"fields": ["windows_os_no"]}),
            ("CPU Info (*Intel*)", {"fields": ["CPU_core", "CPU_generation"]}),
            ("RAM", {"fields": ["ram_size"]}),
            ("Storage", {"fields": ["storage_size", "storage_type"]}),
            ("Video", {"fields": ["screen_size", "screen_port"]}),
            ("Audio", {"fields": ["audio_features"]}),
            ("LAN", {"fields": ["LAN_type"]}),
            ("Battery status", {"fields": ["battery_ok_or_charged"]}),
            ("Installed applications", {"fields": ["installed_apps"]}),
            ("Other", {"fields": ["misc_info"]}),
    ]

admin.site.register(RefurbishedItem, RefurbishedItemAdmin)
