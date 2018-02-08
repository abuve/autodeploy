#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.db.models import Q
from repository import models
from utils.pager import PageInfo
from utils.response import BaseResponse
from django.http.request import QueryDict

from utils.base import BaseServiceList
from repository import models as repository_models
from cmdb import models as CMDB_MODELS

from conf import settings


class Idc(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'name', 'text': 'Idc', 'condition_type': 'input'},
            {'name': 'name', 'text': 'Floor', 'condition_type': 'input'},
            {'name': 'name', 'text': 'Phone', 'condition_type': 'input'},
            {'name': 'name', 'text': 'Address', 'condition_type': 'input'},

        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "Project ID",  # 前端表格中显示的标题
                'display': 0,  # 是否在前端显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'k1':'v1'}  # 自定义属性
            },
            {
                'q': 'name',
                'title': "Name",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@name'}},
                'attr': {}
            },
            {
                'q': 'floor',
                'title': "Floor",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@floor'}},
                'attr': {}
            },
            {
                'q': 'phone',
                'title': "Phone",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@phone'}},
                'attr': {}
            },
            {
                'q': 'idc_address',
                'title': "Address",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@idc_address'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Options",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group">' + \
                                '<a type="button" class="btn btn-default btn-xs" href="/cmdb/edit-idc-{nid}.html"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>' + \
                               '<a type="button" class="btn btn-default btn-xs" onclick=delete_idc_data_fn({nid})><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>' + \
                               '<button type="button" class="btn btn-default dropdown-toggle btn-xs"data-toggle="1dropdown"> <span class="caret"></span> <span class="sr-only">切换下拉菜单</span> </button> <ul class="dropdown-menu" role="menu" style="margin:2px 164px; min-width:130px"> <li><a href="#">More Option</a></li> </ul>' + \
                                '</div>',
                    'kwargs': {'device_type_id': '@device_type_id', 'nid': '@id', 'name': '@name'}},
                'attr': {'width': '300px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            #'server_title': 'select hostname from repository_server where repository_server.asset_id=repository_asset.id and repository_asset.device_type_id=1',
            #'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(Idc, self).__init__(condition_config, table_config, extra_select)



    @staticmethod
    def assets_condition(request):
        con_str = request.GET.get('condition', None)
        if not con_str:
            con_dict = {}
        else:
            con_dict = json.loads(con_str)

        con_q = Q()
        for k, v in con_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con_q.add(temp, 'AND')

        return con_q

    def fetch_idc(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            idc_count = CMDB_MODELS.IDC.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), idc_count)
            idc_list = CMDB_MODELS.IDC.objects.filter(conditions).extra(select=self.extra_select).values(
                *self.values_list).order_by("-id")[page_info.start:page_info.end]
            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(idc_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def delete_data(request):
        response = BaseResponse()
        try:
            recv_data = QueryDict(request.body, encoding='utf-8')
            idc_id = recv_data.get("idc_id")
            CMDB_MODELS.IDC.objects.get(id=idc_id).delete()
            response.message = '删除成功'
        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def add_data(request):
        response = BaseResponse()
        try:
            response.error = []
            post_dict = QueryDict(request.body, encoding='utf-8')

            idc_name = post_dict.get('idc_name')
            idc_floor = post_dict.get('idc_floor')
            idc_phone = post_dict.get('idc_phone')
            idc_address = post_dict.get('idc_address')

            add_to_db = CMDB_MODELS.IDC(
                name=idc_name,
                floor=idc_floor,
                phone=idc_phone,
                idc_address = idc_address,

            )
            add_to_db.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def put_idc(request):
        response = BaseResponse()
        try:
            response.error = []
            put_dict = QueryDict(request.body, encoding='utf-8')
            idc_id = put_dict.get('idc_id')
            idc_name = put_dict.get('idc_name')
            idc_floor = put_dict.get('idc_floor')
            idc_phone = put_dict.get('idc_phone')
            idc_address = put_dict.get('idc_address')

            update_data = CMDB_MODELS.IDC.objects.get(id=idc_id)
            update_data.name = idc_name
            update_data.floor = idc_floor
            update_data.phone = idc_phone
            update_data.idc_address = idc_address
            update_data.save()

        except Exception as e:
            print(Exception,e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def idc_config(idc_id):

        response = BaseResponse()
        try:
            response.data = CMDB_MODELS.IDC.objects.filter(id=idc_id).first()
            # response.asset_data = CMDB_MODELS.Asset.objects.all()
        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response