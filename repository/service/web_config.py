#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os

from django.db.models import Q
from django.http.request import QueryDict

from cmdb import models as CMDB_MODELS
from repository import models as REST_MODELS
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse

from cmdb.service import asset_num

from conf.settings import web_conf_path
from repository.cores import FileHandler


class WebConfig(BaseServiceList):
    def __init__(self):
        pass

    def nginx_config(self, server_id):

        response = BaseResponse()
        try:
            response.data = REST_MODELS.Applications.objects.filter(id=server_id).first()
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def load_tree_data(self, request, server_id):
        response = BaseResponse()
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')
            server_id = post_dict.get('server_id')
            version = post_dict.get('version')

            select_name = post_dict.get('n')
            select_level = post_dict.get('lv')
            select_id = post_dict.get('id')

            file_handler = FileHandler.Manager(server_id, 'nginx', version, select_id)
            ret = file_handler.get_items()

            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)

        return response

    def load_version_data(request, server_id):
        response = BaseResponse()
        try:
            file_handler = FileHandler.Manager(server_id, 'nginx')
            ret = file_handler.get_items()

            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def create_last_version(request, server_id):
        response = BaseResponse()

        file_handler = FileHandler.Manager(server_id, 'nginx')
        response.status = file_handler.create_items('last_version', 'd')
        return response

    def set_last_version(request, server_id):
        response = BaseResponse()
        post_dict = QueryDict(request.body, encoding='utf-8')
        version = post_dict.get('version')
        file_handler = FileHandler.Manager(server_id, 'nginx', version)
        file_handler.set_to_last_version()
        return response

    def get_file(request, server_id):
        response = BaseResponse()
        try:
            get_dict = request.GET
            version = get_dict.get('version')
            select_id = get_dict.get('select_id')
            file_handler = FileHandler.Manager(server_id, 'nginx', version, select_id)
            file_data = file_handler.get_file()
            response.data = file_data
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    def create_file(request, server_id):
        response = BaseResponse()
        try:
            post_dict = QueryDict(request.body, encoding='utf-8')
            print(post_dict)
            obj_name = post_dict.get('create_object_name')
            obj_type = post_dict.get('create_object_type')
            obj_path = post_dict.get('create_object_path')
            version = post_dict.get('version')
            file_handler = FileHandler.Manager(server_id, 'nginx', version)
            exec_status = file_handler.create_items(obj_name, obj_path, obj_type)
            response.data = 1
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response