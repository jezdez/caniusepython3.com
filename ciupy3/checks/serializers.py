from pq.models import Job
from rest_framework import serializers


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('uuid', 'created_at', 'status', 'enqueued_at', 'ended_at',
                  'result', 'if_failed', 'if_result')
