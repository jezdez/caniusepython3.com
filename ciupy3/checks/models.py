from collections import OrderedDict

from django.core import validators
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse
from django.utils.timezone import now

from caniusepython3.__main__ import projects_from_requirements
from django_pg import models
from redis_cache import get_redis_connection

project_name_validator = validators.RegexValidator(r'^[\.\-\w]+$',
                                                   'Project name invalid')


def get_redis():
    return get_redis_connection('default')


class Check(models.Model):
    id = models.UUIDField(auto_add=True, primary_key=True)
    unblocked = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(default=now)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    requirements = models.ArrayField(models.TextField())
    projects = models.ArrayField(models.CharField(max_length=255))
    blockers = models.JSONField()

    def get_absolute_url(self):
        return reverse('check-detail', kwargs={'pk': str(self.pk)})

    def __str__(self):
        return str(self.id)

    def clean(self):
        projects = OrderedDict()  # using this since sets aren't ordered
        for requirement in self.requirements:
            parsed_url_requirement = urlparse(requirement)
            if parsed_url_requirement.scheme in ('http', 'https'):
                try:
                    for project in projects_from_requirements(requirement):
                        projects[project] = None
                except:
                    raise ValidationError("Couldn't check %s." % requirement)
            else:
                projects[requirement] = None
        for project_name in projects.keys():
            project_name_validator(project_name)
        self.projects = projects.keys()
