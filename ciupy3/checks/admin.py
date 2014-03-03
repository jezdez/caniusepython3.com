from django.contrib import admin

from .models import Check


class CheckAdmin(admin.ModelAdmin):
    pass


admin.site.register(Check, CheckAdmin)
