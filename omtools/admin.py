from django.contrib import admin

from omtools import models

from django.contrib.admin import SimpleListFilter

class ProjectFilter(SimpleListFilter):
    title = 'project_id__name'
    parameter_name = 'project_id__name'

    def lookups(self, request, model_admin):
        return [('FPMS'), ('PMS')]

    def queryset(self, request, queryset):
        return queryset.filter(project_id__name=self.value())
        # if self.value() == 'FPMS':
        #     return queryset.filter(project_id__name=self.value())
        # elif self.value() == 'PMS':
        #     return queryset.filter(test_end_date__lt=this_day)


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


