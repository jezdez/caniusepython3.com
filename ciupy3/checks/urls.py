from django.conf.urls import patterns, url

from ciupy3.checks.views import (CheckDetailView, CheckCreateView,
                                 ProjectDetailView)

urlpatterns = patterns('',
    url(r'^$', CheckCreateView.as_view(), name='check_form'),
    url(r'^project/(?P<name>[^/]+)\.(?P<format>(json|svg))$',
        ProjectDetailView.as_view(), name='project-detail'),
    url(r'^check/(?P<pk>[^/]+)\.(?P<format>(json|svg))$',
        CheckDetailView.as_view(), name='check-detail'),
    url(r'^project/(?P<name>[^/]+)$',
        ProjectDetailView.as_view(), name='project-detail'),
    url(r'^check/(?P<pk>[^/]+)$',
        CheckDetailView.as_view(), name='check-detail'),
)
