from django.contrib import admin

from .models import Check, Project


class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'started_at', 'finished_at',
                    'unblocked', 'runs', 'project')
    ordering = ['-created_at']
    raw_id_fields = ['project']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at')
    ordering = ['-created_at']


admin.site.register(Check, CheckAdmin)
admin.site.register(Project, ProjectAdmin)
