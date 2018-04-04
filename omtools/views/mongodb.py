# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:25 AM
# @Author  : Abbott
# @Site    :
# @File    : userprofile.py
# @Software: PyCharm

import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin
from django.http import JsonResponse

from omtools.service import mongodb


class MongodbListView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = mongodb.MongodbConfig.get_template_data()
        return render(request, 'omtools/mongodb.html', {'response': response})


class MongodbJsonView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        response = mongodb.MongodbConfig().fetch_data(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = mongodb.MongodbConfig.data_create(request)
        return HttpResponseRedirect('/omtools/mongodb.html')

    def put(self, request):
        response = mongodb.MongodbConfig.data_update(request)
        return JsonResponse(response.__dict__)


class MongodbDetailView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        response = mongodb.MongodbConfig.get_detail_by_id(request)
        return JsonResponse(response.__dict__)


class MongodbTemplateView(WriteAccessLogsMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        response = mongodb.MongodbConfig.get_template_by_id(request)
        return JsonResponse(response.__dict__)
