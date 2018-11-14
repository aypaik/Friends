from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/dashboard$', views.dashboard),
    url(r'^/add/(?P<id>\d+)$', views.add),
    url(r'^/show/(?P<id>\d+)$', views.show),
    url(r'^/remove/(?P<id>\d+)$', views.remove),
]
