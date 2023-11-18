from django.contrib import admin

from . import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    ...


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "menu", "parent",)
