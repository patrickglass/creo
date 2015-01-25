from django.conf.urls import patterns, include, url
from django.contrib import admin
from creo import views

urlpatterns = patterns('',
    url(r'^$', views.config_index, name='config_index'),
    url(r'^(?P<id>\d+)/$', views.config_display, name='config_display'),
    url(r'^field/$', views.field_index, name='field_index'),
    url(r'^field/(?P<id>\d+)$', views.field_index, name='field_index'),
)
