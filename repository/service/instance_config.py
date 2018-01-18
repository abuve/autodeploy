import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from .base import BaseServiceList
from repository import models as repository_models
from cmdb import models as CMDB_MODELS


class ServerInstance(BaseServiceList):
    def __init__(self):
        pass

    @staticmethod
    def get_asset_instance(server_id):
        response = BaseResponse()
        try:
            response.data = models.Applications.objects.filter(id=server_id).first()
            # 获取project的business，再通过business查找cmdb中对应的资产信息
            response.asset_data = CMDB_MODELS.Asset.objects.filter(
                business_unit__projectinfo__applications__id=server_id)

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_server_instances_json(server_id):
        response = BaseResponse()

        try:
            instance_asset_list = CMDB_MODELS.Asset.objects.filter(instances__app_id=server_id).values('id', 'server__ipaddress',
                                                                                              'device_type_id',
                                                                                              'instances__name',
                                                                                              'instances__app_id__name',
                                                                                              'instances__app_id__project_id__name').order_by("-id")
            response.data = list(instance_asset_list)
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def add_server_instance(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')
            print(post_dict)

            add_instance_group_id = post_dict.get('add_instance_group_id')
            add_instance_id = post_dict.get('add_instance_id')

            add_to_db = repository_models.AppGroups.objects.get(id=add_instance_group_id)
            add_to_db.instance.add(CMDB_MODELS.Asset.objects.get(id=add_instance_id))

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def delete_server_instance(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')
            print(post_dict)

            add_instance_group_id = post_dict.get('add_instance_group_id')
            add_instance_id = post_dict.get('add_instance_id')

            add_to_db = repository_models.AppGroups.objects.get(id=add_instance_group_id)
            add_to_db.instance.remove(CMDB_MODELS.Asset.objects.get(id=add_instance_id))

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def update_server_instance(request):
        response = BaseResponse()
        try:
            response.error = {}
            post_dict = QueryDict(request.body, encoding='utf-8')

            instance_id = post_dict.get('instance_id')
            add_instance_group_id = post_dict.get('add_instance_group_id')
            add_instance_ip = post_dict.get('add_instance_ip')
            add_instance_port = post_dict.get('add_instance_port')

            get_instance_from_db = repository_models.AppInstances.objects.get(id=instance_id)
            get_instance_from_db.group_id = repository_models.AppGroups.objects.get(id=add_instance_group_id)
            get_instance_from_db.ip = add_instance_ip
            get_instance_from_db.port = add_instance_port
            get_instance_from_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def get_instance_by_id(request):
        response = BaseResponse()
        instance_id = request.GET.get('instance_id')
        get_edit_instance_data = repository_models.AppInstances.objects.filter(id=instance_id).values("id", "ip",
                                                                                                      "port",
                                                                                                      "group_id__name",
                                                                                                      "group_id__id")
        response.data = list(get_edit_instance_data)
        print(response.data)
        return response.data
