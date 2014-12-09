from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers
from .models import Check, Project
from .tasks import (get_compatible, get_total,
                    get_checked, get_or_fetch_all_projects)


class PublicDataSerializer(serializers.HyperlinkedModelSerializer):
    compatible = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    checked = serializers.SerializerMethodField()
    public = serializers.SerializerMethodField()

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


class BlockersField(serializers.Field):

    def to_representation(self, data):
        return data


class CheckSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.ListField(child=serializers.CharField())
    blockers = BlockersField(read_only=True)
    requirements = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Check
        fields = ('id', 'created_at', 'started_at', 'finished_at',
                  'requirements', 'projects', 'blockers', 'unblocked')

    def get_last_check(self, obj):
        return obj

    def validate(self, attrs):
        obj = Check(**attrs)
        obj.clean()
        return attrs

    def to_representation(self, obj):
        ret = super(CheckSerializer, self).to_representation(obj)
        ret['projects'] = sorted(ret['projects'])
        if ret['blockers']:
            ret['blockers'] = OrderedDict(sorted(ret['blockers'].items(),
                                                 key=itemgetter(0)))
        return ret


class PublicCheckSerializer(CheckSerializer, PublicDataSerializer):
    class Meta(CheckSerializer.Meta):
        fields = (CheckSerializer.Meta.fields +
                  PublicDataSerializer.Meta.fields)


class ProjectSerializer(PublicDataSerializer):
    finished_at = serializers.DateTimeField(read_only=True,
                                            source='last_check.finished_at')
    check_count = serializers.SerializerMethodField()
    checks = CheckSerializer(read_only=True, many=True)

    def to_representation(self, obj):
        ret = super(ProjectSerializer, self).to_representation(obj)
        number = 0
        checks = []
        for check in ret['checks']:
            if check.get('finished_at', None) is not None:
                checks.append(check)
                number += 1
            if number == 30:
                break
        ret['checks'] = checks
        return ret

    def get_last_check(self, obj):
        return obj.last_check

    def get_check_count(self, obj):
        return obj.checks.exclude(finished_at=None).count()

    class Meta:
        model = Project
        fields = (('id', 'name', 'created_at', 'finished_at',
                   'modified_at', 'checks', 'check_count') +
                  PublicDataSerializer.Meta.fields)
