from django.contrib import admin

from .models import Check


class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'started_at', 'finished_at',
                    'unblocked')
    ordering = ['-created_at']


admin.site.register(Check, CheckAdmin)
