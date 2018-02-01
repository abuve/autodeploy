import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models
from cmdb import models as CMDB_MODELS


class ServerUrlMaps(BaseServiceList):
    def __init__(self):
        pass

    @staticmethod
    def get_server_urlmaps(server_id):
        response = BaseResponse()
        try:
            response.data = models.Applications.objects.filter(id=server_id).first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def get_server_urlmaps_detial(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')
            urlmaps_id = post_dict.get('urlmaps_id')

            get_detail_data = repository_models.UrlConfigHandler.objects.get(id=urlmaps_id)
            response.data = get_detail_data

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_server_urlmaps_json(server_id):
        response = BaseResponse()

        try:
            server_logs_list = repository_models.UrlConfigHandler.objects.filter(group_id__app_id=server_id).values(
                                                                                              'id',
                                                                                              'url',
                                                                                              'memo',
                                                                                              'group_id__name',
                                                                                              'group_id__app_id__name',
                                                                                              'group_id__app_id__project_id__name',
                                                                                              ).order_by("-id")
            response.data = list(server_logs_list)
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def add_urlmaps(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            urlmaps_url = post_dict.get('urlmaps_url')
            urlmaps_group_id = post_dict.get('urlmaps_group_id')
            urlmaps_cloud_id = post_dict.get('urlmaps_cloud_id')
            urlmaps_forward_id = post_dict.get('urlmaps_forward_id')
            urlmaps_instance_id = post_dict.get('urlmaps_instance_id')
            urlmaps_memo = post_dict.get('urlmaps_memo')

            add_to_db = repository_models.UrlConfigHandler(
                group_id_id = urlmaps_group_id,
                url = urlmaps_url,
                memo = urlmaps_memo
            )
            add_to_db.save()

            add_to_db.cloud.add(repository_models.AppGroups.objects.get(id=urlmaps_cloud_id))
            add_to_db.forward.add(repository_models.AppGroups.objects.get(id=urlmaps_forward_id))
            add_to_db.docker.add(repository_models.AppGroups.objects.get(id=urlmaps_instance_id))

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def delete_urlmaps(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')
            urlmaps_id = post_dict.get('urlmaps_id')

            data_from_db = repository_models.UrlConfigHandler.objects.get(id=urlmaps_id)
            data_from_db.delete()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    def update_urlmaps(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            urlmaps_id = post_dict.get('urlmaps_id')
            urlmaps_url = post_dict.get('urlmaps_url')
            urlmaps_group_id = post_dict.get('urlmaps_group_id')
            urlmaps_cloud_id = post_dict.get('urlmaps_cloud_id')
            urlmaps_forward_id = post_dict.get('urlmaps_forward_id')
            urlmaps_instance_id = post_dict.get('urlmaps_instance_id')
            urlmaps_memo = post_dict.get('urlmaps_memo')

            get_data_from_db = repository_models.UrlConfigHandler.objects.get(id=urlmaps_id)
            get_data_from_db.group_id_id = urlmaps_group_id
            get_data_from_db.url = urlmaps_url
            get_data_from_db.memo = urlmaps_memo
            get_data_from_db.save()

            get_data_from_db.cloud.clear()
            get_data_from_db.forward.clear()
            get_data_from_db.docker.clear()

            get_data_from_db.cloud.add(repository_models.AppGroups.objects.get(id=urlmaps_cloud_id))
            get_data_from_db.forward.add(repository_models.AppGroups.objects.get(id=urlmaps_forward_id))
            get_data_from_db.docker.add(repository_models.AppGroups.objects.get(id=urlmaps_instance_id))

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_urlmaps_by_id(request):
        response = BaseResponse()
        urlmaps_id = request.GET.get('urlmaps_id')
        get_edit_urlmaps_data = repository_models.UrlConfigHandler.objects.filter(id=urlmaps_id).values("id", "group_id_id", "url", "cloud__id", "forward__id", "docker__id", "memo")
        print(list(get_edit_urlmaps_data))
        response.data = list(get_edit_urlmaps_data)
        return response.data
