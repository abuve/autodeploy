# -*- coding: utf-8 -*-

import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin
from django.http import JsonResponse

from omtools.service import logs
from repository import models as REPOSITORY_MODELS
from omtools.models import LogsControl


class LogsIndexView(WriteAccessLogsMixin, LoginRequiredMixin, View):
    def get(self, request):
        response = REPOSITORY_MODELS.ProjectInfo.objects.filter(name__in=['FPMS', 'PMS'])
        return render(request, 'omtools/logs_index.html', {'response': response})

    def post(self, request):
        response = mongodb.MongodbConfig.do_approval_by_id(request)
        return HttpResponseRedirect('/omtools/mongodb-approval.html?id=%s' % response.data.approval_md5)


class LogsDetailView(WriteAccessLogsMixin, LoginRequiredMixin, View):
    def get(self, request, project_id):
        response = REPOSITORY_MODELS.ProjectInfo.objects.get(id=project_id)
        response = LogsControl.objects.filter(project_id__id=project_id).order_by('server_node', '-server_type')
        return render(request, 'omtools/logs_detail.html', {'response': response})