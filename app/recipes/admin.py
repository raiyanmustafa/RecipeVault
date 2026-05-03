from django.contrib import admin

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "description", "ingredients", "notes")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
