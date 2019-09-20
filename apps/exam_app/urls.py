from django.conf.urls import url
from . import views   

urlpatterns = [ 
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^trips/new$', views.new_trip),
    url(r'^remove/(?P<num>\d+)$', views.remove),
    url(r'^trips/edit/(?P<num>\d+)$', views.edit),
    url(r'^join/(?P<num>\d+)$', views.join),
    url(r'^trip_create$', views.trip_create),
    url(r'^trip_update/(?P<num>\d+)$', views.trip_update),
    url(r'^cancel$', views.cancel),
    url(r'^trips/(?P<num>\d+)$', views.one_trip),
    url(r'^go_back$', views.go_back),
    url(r'^move/(?P<num>\d+)$$', views.move_to_bottom),
]