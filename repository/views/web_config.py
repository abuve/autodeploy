#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from repository.service import web_config


class WebConfigNginxView(LoginRequiredMixin, View):
    def get(self, request, server_id):
        response = web_config.WebConfig().nginx_config(server_id)
        return render(request, 'server_config_nginx.html', {'response': response})


class WebConfigNginxJsonView(LoginRequiredMixin, View):
    def post(self, request, server_id):
        response = web_config.WebConfig().load_tree_data(request, server_id)
        return HttpResponse(json.dumps(response.data))


class WebConfigVersionJsonView(LoginRequiredMixin, View):
    def get(self, request, server_id):
        response = web_config.WebConfig.load_version_data(request, server_id)
        return JsonResponse(response.__dict__)

    def post(self, request, server_id):
        response = web_config.WebConfig.create_last_version(request, server_id)
        return JsonResponse(response.__dict__)

    def put(self, request, server_id):
        response = web_config.WebConfig.set_last_version(request, server_id)
        return JsonResponse(response.__dict__)

class WebConfigVersionListView(LoginRequiredMixin, View):
    def get(self, request, server_id):
        response = web_config.WebConfig.get_version_tree(server_id)
        return JsonResponse(response.__dict__)


class WebConfigFileData(LoginRequiredMixin, View):
    def get(self, request, server_id):
        response = web_config.WebConfig.get_file(request, server_id)
        return JsonResponse(response.__dict__)

    def post(self, request, server_id):
        response = web_config.WebConfig.create_file(request, server_id)
        return JsonResponse(response.__dict__)

    def delete(self, request, server_id):
        response = web_config.WebConfig.delete_file(request, server_id)
        return JsonResponse(response.__dict__)

    def put(self, request, server_id):
        response = web_config.WebConfig.edit_file(request, server_id)
        return JsonResponse(response.__dict__)


class WebConfigFilePush(LoginRequiredMixin, View):
    def post(self, request, server_id):
        response = web_config.WebConfig.push_file(request, server_id)
        return JsonResponse(response.__dict__)


class WebConfigVersionStatus(LoginRequiredMixin, View):
    def post(self, request):
        response = web_config.WebConfig.get_version_status(request)
        return render(request, 'include/server_config_webconfig_right_status.html', {'response': response})
