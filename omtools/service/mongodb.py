#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from django.db.models import Q
from django.http.request import QueryDict

from omtools import models as OMTOOLS_MODELS
from utils.base import BaseServiceList
from utils.pager import PageInfo
from utils.response import BaseResponse


class MongodbConfig(BaseServiceList):
    def __init__(self):
        # 查询条件的配置
        condition_config = [
            {'name': 'url_name', 'text': 'URL Name', 'condition_type': 'input'},
            {'name': 'url_method', 'text': 'URL Method', 'condition_type': 'select', 'global_name': 'url_method_list'},
        ]
        # 表格的配置
        table_config = [
            {
                'q': 'id',  # 用于数据库查询的字段，即Model.Tb.objects.filter(*[])
                'title': "ID",  # 前段表格中显示的标题
                'display': 0,  # 是否在前段显示，0表示在前端不显示, 1表示在前端隐藏, 2表示在前段显示
                'text': {'content': "{id}", 'kwargs': {'id': '@id'}},
                'attr': {'k1': 'v1'}  # 自定义属性
            },
            {
                'q': 'title',
                'title': "Mission Name",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@title'}},
                'attr': {}
            },
            {
                'q': 'op_type',
                'title': "Mission Type",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@@op_type_list'}},
                'attr': {}
            },
            {
                'q': 'req_user__username',
                'title': "Request User",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@req_user__username'}},
                'attr': {}
            },
            {
                'q': 'op_user__username',
                'title': "Option User",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@op_user__username'}},
                'attr': {}
            },
            {
                'q': 'status',
                'title': "Status",
                'display': 1,
                'text': {'content': '<a type="button" class="btn btn-{class} btn-xs">{n}</a>',
                         'kwargs': {'n': '@@option_status', 'class': '@@status_map'}
                         },
                'attr': {}
            },
            {
                'q': 'date',
                'title': "Date",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@date'}},
                'attr': {}
            },
            {
                'q': 'memo',
                'title': "Memo",
                'display': 1,
                'text': {'content': "{n}", 'kwargs': {'n': '@memo'}},
                'attr': {}
            },
            {
                'q': None,
                'title': "Options",
                'display': 1,
                'text': {
                    'content': '<div class="btn-group"><a type="button" class="btn btn-default btn-xs" onclick="show_mission_detail_fn({nid})"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Details</a><a type="button" class="btn btn-default btn-xs" onclick="submit_mission_fn({nid})"><span class="glyphicon glyphicon-check" aria-hidden="true"></span> Submit</a></div>',
                    'kwargs': {'nid': '@id'}},
                'attr': {'style': 'text-align: left; width: 260px'}
            },
        ]
        # 额外搜索条件
        extra_select = {
            'server_title': '',
            # 'network_title': 'select management_ip from repository_networkdevice where repository_networkdevice.asset_id=repository_asset.id and repository_asset.device_type_id=2',
        }
        super(MongodbConfig, self).__init__(condition_config, table_config, extra_select)

    @property
    def op_type_list(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, OMTOOLS_MODELS.MongodbMission.op_type_choices)
        return list(result)

    @property
    def option_status(self):
        result = map(lambda x: {'id': x[0], 'name': x[1]}, OMTOOLS_MODELS.MongodbMission.status_choices)
        return list(result)

    @property
    def status_map(self):
        result = [
            {'id': 1, 'name': 'success'},
            {'id': 2, 'name': 'danger'},
            # {'id': 3, 'name': 'danger'},
        ]
        return result

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

    def fetch_data(self, request):
        response = BaseResponse()
        try:
            ret = {}
            conditions = self.assets_condition(request)
            asset_count = OMTOOLS_MODELS.MongodbMission.objects.filter(conditions).count()
            page_info = PageInfo(request.GET.get('pager', None), asset_count)
            asset_list = OMTOOLS_MODELS.MongodbMission.objects.filter(conditions).order_by('-id').extra(
                select=self.extra_select).values(
                *self.values_list)[page_info.start:page_info.end]

            ret['table_config'] = self.table_config
            ret['condition_config'] = self.condition_config
            ret['data_list'] = list(asset_list)
            ret['page_info'] = {
                "page_str": page_info.pager(),
                "page_start": page_info.start,
            }
            ret['global_dict'] = {
                'op_type_list': self.op_type_list,
                'option_status': self.option_status,
                'status_map': self.status_map,
            }
            response.data = ret
            response.message = '获取成功'
        except Exception as e:
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def data_create(request):
        response = BaseResponse()
        try:
            post_data = QueryDict(request.body, encoding='utf-8')
            mongoMission_title = post_data.get('mongoMission_title')
            mongoMission_memo = post_data.get('mongoMission_memo')
            option_exec = "db.proposal.update({'proposalId': $1 }, {$set: {'status': $2 }})"

            for k,v in post_data.items():
                if '_var' in k:
                    var_count = k.split('mongoMission_var_')[1]
                    var = post_data.get('mongoMission_var_%s' % var_count)
                    var_type = post_data.get('mongoMission_v_type_%s' % var_count)
                    if var_type == 'LIST':
                        var = str(var.split('\r\n'))
                    option_exec = option_exec.replace('$%s' % var_count, var)

            # 创建Mission
            data_obj = OMTOOLS_MODELS.MongodbMission(
                title = mongoMission_title,
                op_exec = option_exec,
                req_user_id = request.user.id,
                memo = mongoMission_memo
            )
            data_obj.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)

        return response

    @staticmethod
    def data_update(request):
        response = BaseResponse()
        try:
            put_data = QueryDict(request.body, encoding='utf-8')
            obj_id = put_data.get('id')

            update_data = OMTOOLS_MODELS.MongodbMission.objects.get(id=obj_id)
            update_data.op_user_id = request.user.id
            update_data.status = 1
            update_data.save()

        except Exception as e:
            print(Exception, e)
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_permission_data():

        response = BaseResponse()
        try:
            response.data = USER_CENTER_MODELS.Permission.objects.all().order_by('-id')

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response

    @staticmethod
    def get_detail_by_id(request):
        response = BaseResponse()
        try:
            obj_id = request.GET.get('id')
            response.data = OMTOOLS_MODELS.MongodbMission.objects.filter(id=obj_id).values().first()

        except Exception as e:
            response.status = False
            response.message = str(e)
        return response
