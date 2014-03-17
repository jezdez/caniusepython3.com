from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers
from .models import Check
from .jobs import get_compatible, get_total, get_checked, get_or_fetch_all_projects


class CheckSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.SerializerMethodField('get_projects')
    blockers = serializers.SerializerMethodField('get_blockers')
    requirements = serializers.CharField('requirements')
    compatible = serializers.SerializerMethodField('get_compatible')
    total = serializers.SerializerMethodField('get_total')
    checked = serializers.SerializerMethodField('get_checked')
    public = serializers.SerializerMethodField('get_public')

    class Meta:
        model = Check
        fields = ('id', 'created_at', 'started_at', 'finished_at',
                  'requirements', 'projects', 'blockers', 'unblocked',
                  'compatible', 'total', 'checked', 'public')

    def get_projects(self, obj):
        return sorted(obj.projects)

    def get_blockers(self, obj):
        if obj.blockers:
            return OrderedDict(sorted(obj.blockers.items(),
                                      key=itemgetter(0)))
        else:
            return {}

    def get_compatible(self, obj):
        return int(get_compatible() or 0)

    def get_total(self, obj):
        return int(get_total() or 0)

    def get_checked(self, obj):
        return int(get_checked() or 0)

    def get_public(self, obj):
        all_projects = get_or_fetch_all_projects(lower=True)
        return all_projects.intersection(set([project.lower()
                                              for project in obj.projects]))
