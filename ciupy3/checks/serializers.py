from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers
from .models import Check, Project
from .jobs import (get_compatible, get_total,
                   get_checked, get_or_fetch_all_projects)


class PublicDataSerializer(serializers.HyperlinkedModelSerializer):
    compatible = serializers.SerializerMethodField('get_compatible')
    total = serializers.SerializerMethodField('get_total')
    checked = serializers.SerializerMethodField('get_checked')
    public = serializers.SerializerMethodField('get_public')

    class Meta:
        fields = ('compatible', 'total', 'checked', 'public')

    def get_compatible(self, obj):
        return int(get_compatible() or 0)

    def get_total(self, obj):
        return int(get_total() or 0)

    def get_checked(self, obj):
        return int(get_checked() or 0)

    def get_last_check(self, obj):
        raise NotImplementedError

    def get_public(self, obj):
        check = self.get_last_check(obj)
        if check is None:
            return []
        all_projects = get_or_fetch_all_projects(lower=True)
        check_project_set = set([project.lower()
                                for project in check.projects])
        return set(all_projects.keys()).intersection(check_project_set)


class CheckSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.CharField()
    blockers = serializers.CharField()
    requirements = serializers.CharField()

    class Meta:
        model = Check
        fields = ('id', 'created_at', 'started_at', 'finished_at',
                  'requirements', 'projects', 'blockers', 'unblocked')

    def get_last_check(self, obj):
        return obj

    def transform_projects(self, obj, value):
        return sorted(value)

    def transform_blockers(self, obj, value):
        if value:
            return OrderedDict(sorted(value.items(),
                                      key=itemgetter(0)))
        return value


class PublicCheckSerializer(CheckSerializer, PublicDataSerializer):
    class Meta(CheckSerializer.Meta):
        fields = (CheckSerializer.Meta.fields +
                  PublicDataSerializer.Meta.fields)


class ProjectSerializer(PublicDataSerializer):
    finished_at = serializers.SerializerMethodField('get_finished_at')
    checks = CheckSerializer(read_only=True, many=True)

    def transform_checks(self, obj, value):
        return value[:20]

    def get_last_check(self, obj):
        return obj.last_check

    def get_finished_at(self, obj):
        if obj.last_check:
            return obj.last_check.finished_at
        return None

    class Meta:
        model = Project
        fields = (('id', 'name', 'created_at', 'finished_at',
                   'modified_at', 'checks') +
                  PublicDataSerializer.Meta.fields)
