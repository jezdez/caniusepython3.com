from django.conf.urls import patterns, include, url
from rest_framework import routers
from ciupy3.checks.views import CheckViewSet, CheckCreateView, ProjectViewSet

from django.contrib import admin
admin.autodiscover()


class APIRouter(routers.DefaultRouter):
    include_root_view = False

router = APIRouter(trailing_slash=False)
router.register(r'check', CheckViewSet)
router.register(r'project', ProjectViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^$', CheckCreateView.as_view(), name='check_form'),
    url(r'^', include(router.urls)),
    url(r'^admin/', include('admin_honeypot.urls')),
    url(r'^manage/rq/', include('django_rq.urls')),
    url(r'^manage/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
)
