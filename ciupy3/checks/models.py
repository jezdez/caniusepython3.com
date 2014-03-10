import re
from collections import OrderedDict

from django.core import validators
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.timezone import now

from caniusepython3.__main__ import projects_from_requirements
from django_pg import models
from redis_cache import get_redis_connection

project_name_re = re.compile(r'^[\.\-\w]+$')




def get_redis():
    return get_redis_connection('default')


def sanitize_github_url(requirement, url):
    if url.netloc == 'github.com':
        split_path = list(filter(None, url.path.split('/')))
        if len(split_path) > 4:  # github.com/<user>/<repo>/blob/<branch>
            if split_path[2] == 'blob':
                split_path[2] = 'raw'
            path = '/' + '/'.join(split_path)
            requirement = urlunparse((url.scheme, url.netloc, path,
                                      url.params, url.query, url.fragment))
    return requirement


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
            url = urlparse(requirement)
            if url.scheme in ('http', 'https'):
                requirement = sanitize_github_url(requirement, url)
                try:
                    for project in projects_from_requirements(requirement):
                        projects[project] = None
                except:
                    raise ValidationError("Couldn't check %s." % requirement)
            else:
                projects[requirement] = None
        for project_name in projects.keys():
            validators.RegexValidator(project_name_re,
                                      'Project %s invalid' %
                                      project_name)(project_name)
        self.projects = projects.keys()
