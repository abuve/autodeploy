from django.conf.urls import url
from repository.views import web_config

urlpatterns = [

    url(r'^webconf/nginx/config-(?P<server_id>\d+).html$', web_config.WebConfigNginxView.as_view()),
    url(r'^webconf/nginx/fileTreeJson-(?P<server_id>\d+).html$', web_config.WebConfigNginxJsonView.as_view()),

    url(r'^webconf/nginx/version-json-(?P<server_id>\d+).html$', web_config.WebConfigVersionJsonView.as_view()),

    url(r'^webconf/nginx/file-data-(?P<server_id>\d+).html$', web_config.WebConfigFileData.as_view()),

]
