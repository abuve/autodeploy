from django.conf.urls import url
from omtools.views import mongodb

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^mongodb.html$', mongodb.MongodbListView.as_view(), name='omtools-mongodb-list'),
    url(r'^mongodb-json.html$', mongodb.MongodbJsonView.as_view(), name='omtools-mongodb-json'),
    url(r'^mongodb-get-detail.html$', mongodb.MongodbDetailView.as_view(), name='omtools-mongodb-detail'),

]
