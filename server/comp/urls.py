from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('comp.views',
    url(r'^$', 'index'),
)
