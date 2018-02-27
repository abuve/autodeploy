# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:18 AM
# @Author  : Abbott
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url

from user_center.views import userprofile, usergroups

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^user-list.html$', userprofile.UserProfileListView.as_view()),
    url(r'^users.html$', userprofile.UserJsonView.as_view()),
    url(r'^edit-user-(?P<user_id>\d+).html$', userprofile.UpdateUserView.as_view()),

    url(r'^group-list.html$', usergroups.GroupProfileListView.as_view()),
    url(r'^groups.html$', usergroups.GroupJsonView.as_view()),
    url(r'^add-group.html$', usergroups.AddGroupView.as_view()),
    url(r'^edit-group-(?P<group_id>\d+).html$', usergroups.UpdateGroupView.as_view()),
]
