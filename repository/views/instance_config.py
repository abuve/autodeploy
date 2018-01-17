#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from repository.service import web_config
from repository.service import instance_config


class InstanceConfigView(View):
    def get(self, request, server_id):
        response = instance_config.ServerInstance.get_asset_instance(server_id)
        return render(request, 'server_config_instance.html', {'response': response})


class InstanceConfigJsonView(View):
    def get(self, request, server_id):
        response = instance_config.ServerInstance.get_server_instances_json(server_id)
        return HttpResponse(json.dumps(response.data))