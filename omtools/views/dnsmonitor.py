# -*- coding: utf-8 -*-

import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin, WriteAccessLogsMixin
from django.http import JsonResponse

from omtools.service import logs
from repository import models as REPOSITORY_MODELS
from omtools.models import DnsMonitorControl
from django.http.request import QueryDict


class DnsMonitorIndexView(WriteAccessLogsMixin, View):
    def get(self, request):
        response = DnsMonitorControl.objects.all().order_by('-project_id__name')
        return render(request, 'omtools/dnsmonitor_index.html', {'response': response})

    def post(self, request):
        request_data = request.body.decode('utf-8')
        request_json = json.loads(request_data)
        domain = request_json.get('domain')
        pro_name = request_json.get('pro_name')
        obj_from_db = DnsMonitorControl.objects.get_or_create(domain=domain)[0]
        obj_from_db.node1_status = False
        obj_from_db.project_id = REPOSITORY_MODELS.ProjectInfo.objects.get(name=pro_name)
        obj_from_db.save()
        return HttpResponse(1)
