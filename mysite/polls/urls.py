#!/usr/bin/env python
from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^create_poll/$', views.PollCreationView.as_view(), name='poll_creation'),
    url(r'^submit_poll/$', views.submit_poll, name='submit_poll'),
    url(r'^(?P<number>\d+)/(?P<poll_id>\d+)$', views.create_options, name='option_creation'),
    url(r'^submit_options/$', views.submit_options, name='submit_options'),
)
