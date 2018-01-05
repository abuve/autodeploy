from django.conf.urls import url

from cmdb.views import server
from cmdb.views import approval
from cmdb.views import docker
from cmdb.views import business

urlpatterns = [
    url(r'^$', server.ServerListView.as_view()),
    url(r'^server-list.html$', server.ServerListView.as_view()),
    url(r'^server-json.html$', server.ServerJsonView.as_view()),

    url(r'^asset-create.html$', server.AssetCreateView.as_view()),

    url(r'^docker-list.html$', docker.DockerListView.as_view()),
    url(r'^docker-json.html$', docker.DockerJsonView.as_view()),

    url(r'^asset-detail-(?P<asset_nid>\d+).html$', server.AssetDetailView.as_view()),

    url(r'^approval-list.html$', approval.ApprovalListView.as_view()),
    url(r'^approval-json.html$', approval.ApprovalJsonView.as_view()),

    url(r'^business-list.html$', business.BusinessListView.as_view()),
    url(r'^business-json.html$', business.BusinessJsonView.as_view()),
    url(r'^business-detail-(?P<business_nid>\d+).html$', business.BusinessDetailView.as_view()),

    # cmdb report with no asset id, it's need admin to approved.
    #url(r'^report/asset_report_use_asset_id/$', approval.asset_report_use_asset_id),
    #url(r'^report/asset_report_with_no_id/$', approval.asset_with_no_asset_id),

    url(r'^get_instance_by_asset_id/$', approval.asset_with_no_asset_id),

    url(r'^test/$', server.test),

    url(r'^rsync_old_data/$', server.rsync_old_data),

    url(r'^upload_cloud_server/$', server.upload_cloud_server),

]
