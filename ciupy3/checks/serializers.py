from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers
from .models import Check
from .jobs import get_compatible


class CheckSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.SerializerMethodField('get_projects')
    blockers = serializers.SerializerMethodField('get_blockers')
    requirements = serializers.CharField('requirements')
    compatible = serializers.SerializerMethodField('get_compatible')

    class Meta:
        model = Check
        fields = ('id', 'created_at', 'started_at', 'finished_at',
                  'requirements', 'projects', 'blockers', 'unblocked',
                  'compatible')

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
