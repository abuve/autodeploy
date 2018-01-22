from django.conf.urls import url
from repository.views import web_config
from repository.views import group_config
from repository.views import instance_config

from django.contrib.auth.decorators import login_required

urlpatterns = [

    url(r'^webconf/nginx/config-(?P<server_id>\d+).html$', login_required(web_config.WebConfigNginxView.as_view())),
    url(r'^webconf/nginx/fileTreeJson-(?P<server_id>\d+).html$', login_required(web_config.WebConfigNginxJsonView.as_view())),
    url(r'^webconf/nginx/version-json-(?P<server_id>\d+).html$', login_required(web_config.WebConfigVersionJsonView.as_view())),
    url(r'^webconf/nginx/version-tree-(?P<server_id>\d+).html$', login_required(web_config.WebConfigVersionListView.as_view())),
    url(r'^webconf/nginx/file-data-(?P<server_id>\d+).html$', login_required(web_config.WebConfigFileData.as_view())),
    url(r'^webconf/nginx/file-push-(?P<server_id>\d+).html$', login_required(web_config.WebConfigFilePush.as_view())),

    url(r'^webconf/nginx/get_version_status.html$', login_required(web_config.WebConfigVersionStatus.as_view())),

    url(r'^config/group/(?P<server_id>\d+).html$', login_required(group_config.GroupConfigView.as_view())),
    url(r'^config/group/json-(?P<server_id>\d+).html$', login_required(group_config.GroupConfigJsonView.as_view())),
    url(r'^config/group/update-server-group.html$', login_required(group_config.UpdateServerGroupView.as_view())),

    url(r'^config/instance/(?P<server_id>\d+).html$', login_required(instance_config.InstanceConfigView.as_view())),
    url(r'^config/instance/json-(?P<server_id>\d+).html$', login_required(instance_config.InstanceConfigJsonView.as_view())),
    url(r'^config/instance/update-server-instance.html$', login_required(instance_config.UpdateServerInstanceView.as_view())),

]
