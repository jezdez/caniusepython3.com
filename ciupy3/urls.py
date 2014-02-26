from django.conf.urls import patterns, include, url
from rest_framework import routers
from ciupy3.checks.views import JobViewSet, CheckCreateView, CheckDetailView

from django.contrib import admin
admin.autodiscover()


class APIRouter(routers.DefaultRouter):
    include_root_view = False

router = APIRouter(trailing_slash=False)
router.register(r'jobs', JobViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^$', CheckCreateView.as_view(), name='check_form'),
    url(r'^check/(?P<uuid>[-\w]+)$',
        CheckDetailView.as_view(), name='check_detail'),
    url(r'^', include(router.urls)),
    url(r'^manage/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
