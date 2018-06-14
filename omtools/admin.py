from django.contrib import admin

from omtools import models


class AccessLogsControl(admin.ModelAdmin):
    list_display = (
        'project_id', 'server_ip', 'server_node', 'server_type', 'logs_type', 'url', 'logs_status', 'order_value',
        'memo')
    search_fields = ('server_node', 'server_ip', 'server_type', 'logs_type', 'url', 'memo')
    list_display_links = ('project_id', 'server_ip', 'server_node', 'server_type', 'logs_type', 'url', 'memo')
    list_editable = ['logs_status', 'order_value']
    list_filter = ('project_id', 'server_ip', 'server_node', 'server_type', 'logs_status')

admin.site.site_header = 'OM CMDB Admin'
admin.site.site_title = 'OM CMDB Admin'

admin.site.register(models.MongodbMission)
admin.site.register(models.MongodbMissionTemplate)
admin.site.register(models.LogsControl, AccessLogsControl)