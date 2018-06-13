from django.contrib import admin

from omtools import models

class AccessLogsControl(admin.ModelAdmin):
    list_display = ('project_id', 'server_node', 'server_type', 'logs_type', 'url', 'memo')
    search_fields = ('server_node', 'server_type', 'logs_type', 'url', 'memo')


admin.site.register(models.MongodbMission)
admin.site.register(models.MongodbMissionTemplate)
admin.site.register(models.LogsControl, AccessLogsControl)