from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web.views import account
from web.views import home
from web.views import asset
from web.views import user
from web.views import server
from web.views import mission

urlpatterns = [
    # url(r'^login.html$', account.LoginView.as_view()),
    # url(r'^logout.html$', account.LogoutView.as_view()),
    # url(r'^index.html$', home.IndexView.as_view()),
    # url(r'^cmdb.html$', home.CmdbView.as_view()),
    #
    # url(r'^asset.html$', asset.AssetListView.as_view()),
    # url(r'^assets.html$', asset.AssetJsonView.as_view()),
    #
    # url(r'^idc.html$', asset.IDCListView.as_view()),
    # url(r'^idcjson.html$', asset.IDCJsonView.as_view()),
    #
    # url(r'^asset-(?P<device_type_id>\d+)-(?P<asset_nid>\d+).html$', asset.AssetDetailView.as_view()),
    # url(r'^add-asset.html$', asset.AddAssetView.as_view()),
    #
    # url(r'^users.html$', user.UserListView.as_view()),
    # url(r'^user.html$', user.UserJsonView.as_view()),


    url(r'^server.html$', server.ServerListView.as_view()),
    url(r'^servers.html$', server.ServerJsonView.as_view()),
    url(r'^server-config-(?P<asset_nid>\d+).html$', server.ServerDetailView.as_view(), name='server-config'),
    url(r'^add-server.html$', server.AddServerView.as_view()),
    url(r'^edit-server-(?P<server_nid>\d+).html$', server.UpdateServerView.as_view()),

    url(r'^get_app_by_project/$', server.get_app_by_project),

    url(r'^update-server-group.html$', server.UpdateServerGroupView.as_view()),
    url(r'^server-groups-(?P<asset_nid>\d+).html$', server.ServerDetaiGroupView.as_view()),

    url(r'^server-instances-(?P<asset_nid>\d+).html$', server.ServerDetaiInstanceView.as_view()),
    url(r'^update-server-instance.html$', server.UpdateServerInstanceView.as_view()),
    url(r'^get-server-instance_type.html$', server.GetServerInstanceTypeView.as_view()),

    url(r'^update-yaml-nginx.html$', server.UpdateYamlConfView.as_view()),

    url(r'^mission.html$', mission.MissionListView.as_view()),
    url(r'^missions.html$', mission.MissionJsonView.as_view()),
    url(r'^mission-create.html$', mission.MissionCreateView.as_view()),
    url(r'^mission-detail-(?P<mission_id>\d+).html$', mission.MissionDetailListView.as_view()),
    url(r'^mission-detail-json-(?P<mission_id>\d+).html$', mission.MissionDetailListJsonView.as_view()),

    url(r'^mission-detail-json-(?P<mission_id>\d+).html$', mission.MissionDetailListJsonView.as_view()),

    # url(r'^chart-(?P<chart_type>\w+).html$', home.ChartView.as_view()),
]
