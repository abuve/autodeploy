from django.conf.urls import url
from repository.views import web_config
from repository.views import instance_config

urlpatterns = [

    url(r'^webconf/nginx/config-(?P<server_id>\d+).html$', web_config.WebConfigNginxView.as_view()),
    url(r'^webconf/nginx/fileTreeJson-(?P<server_id>\d+).html$', web_config.WebConfigNginxJsonView.as_view()),
    url(r'^webconf/nginx/version-json-(?P<server_id>\d+).html$', web_config.WebConfigVersionJsonView.as_view()),
    url(r'^webconf/nginx/version-tree-(?P<server_id>\d+).html$', web_config.WebConfigVersionListView.as_view()),
    url(r'^webconf/nginx/file-data-(?P<server_id>\d+).html$', web_config.WebConfigFileData.as_view()),
    url(r'^webconf/nginx/file-push-(?P<server_id>\d+).html$', web_config.WebConfigFilePush.as_view()),

    url(r'^webconf/nginx/get_version_status.html$', web_config.WebConfigVersionStatus.as_view()),

    url(r'^config/instance/(?P<server_id>\d+).html$', instance_config.InstanceConfigView.as_view()),
    url(r'^config/instance/json-(?P<server_id>\d+).html$', instance_config.InstanceConfigJsonView.as_view()),

]
