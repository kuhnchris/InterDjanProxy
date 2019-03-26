from django.contrib import admin
from .models import menuItem, portalItem

@admin.decorators.register(menuItem)
class menuItemAdmin(admin.ModelAdmin):
    pass


@admin.decorators.register(portalItem)
class portalItemAdmin(admin.ModelAdmin):
    pass
