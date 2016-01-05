from django.conf.urls import url

from ciupy3.checks.views import (CheckDetailView, CheckCreateView,
                                 ProjectDetailView, autocomplete)

urlpatterns = [
    url(r'^$', CheckCreateView.as_view(), name='check_form'),
    url(r'^autocomplete/$', autocomplete, name='project-autocomplete'),
    url(r'^project/(?P<name>[^/]+)\.(?P<format>(json|svg|png))$',
        ProjectDetailView.as_view(), name='project-detail'),
    url(r'^check/(?P<pk>[^/]+)\.(?P<format>(json|svg|png))$',
        CheckDetailView.as_view(), name='check-detail'),
    url(r'^project/(?P<name>[^/]+)$',
        ProjectDetailView.as_view(), name='project-detail'),
    url(r'^check/(?P<pk>[^/]+)$',
        CheckDetailView.as_view(), name='check-detail'),
]
