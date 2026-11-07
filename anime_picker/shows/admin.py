from django.contrib import admin

from .models import Show


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ("name", "media_type", "genre", "status", "created_at")
    list_filter = ("media_type", "status", "genre")
    search_fields = ("name",)
