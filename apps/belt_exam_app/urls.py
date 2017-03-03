from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'home'),
    url(r'^create$', views.create, name = 'create'),
    url(r'^add/(?P<id>\d+)$', views.add, name = 'add'),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = 'remove'),
    url(r'^user/(?P<id>\d+)$', views.user, name = 'user')
]
