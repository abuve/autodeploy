from django.conf.urls import url
from system.views import page_control

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^403.html$', page_control.PermissionDeniedView.as_view(), name='page-control-403'),
]
