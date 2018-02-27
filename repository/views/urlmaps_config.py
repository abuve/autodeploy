#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.views import View
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from repository.service import urlmaps_config


class UrlMapsConfigView(LoginRequiredMixin, View):
    def get(self, request, server_id):
        response = urlmaps_config.ServerUrlMaps.get_server_urlmaps(server_id)
        return render(request, 'server_config_urlmaps.html', {'response': response})


class UrlMapsDetailView(LoginRequiredMixin, View):
    def post(self, request):
        response = urlmaps_config.ServerUrlMaps.get_server_urlmaps_detial(request)
        return render(request, 'include/server_config_urlmaps_detail.html', {'response': response})


class UrlMapsConfigJsonView(LoginRequiredMixin, View):
    def get(self, request, server_id):
        response = urlmaps_config.ServerUrlMaps.get_server_urlmaps_json(server_id)
        return HttpResponse(json.dumps(response.data))


class UpdateUrlMapsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = urlmaps_config.ServerUrlMaps.get_urlmaps_by_id(request)
        return HttpResponse(json.dumps(response))

    def post(self, request):
        response = urlmaps_config.ServerUrlMaps.add_urlmaps(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = urlmaps_config.ServerUrlMaps.update_urlmaps(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = urlmaps_config.ServerUrlMaps.delete_urlmaps(request)
        return JsonResponse(response.__dict__)


class UpdateUrlMapsGroupsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = urlmaps_config.ServerUrlMaps.get_urlmaps_groups_by_id(request)
        return JsonResponse(response.__dict__)

    def post(self, request):
        response = urlmaps_config.ServerUrlMaps.update_urlmaps_groups(request)
        return JsonResponse(response.__dict__)
