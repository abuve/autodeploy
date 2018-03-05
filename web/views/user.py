#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from utils.mixin_utils import LoginRequiredMixin, PermissionRequiredMixin

from web.service import user


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users_list.html')


class UserJsonView(LoginRequiredMixin, PermissionRequiredMixin, View):
    def get(self, request):
        obj = user.User()
        response = obj.fetch_users(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = user.User.delete_users(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = user.User.put_users(request)
        return JsonResponse(response.__dict__)
