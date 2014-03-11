import re
from collections import OrderedDict

from pip.req import parse_requirements
from pip.index import PackageFinder

from django.core import validators
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.timezone import now


from django_pg import models
from redis_cache import get_redis_connection

project_name_re = re.compile(r'^[\.\-\w]+$')
index_urls = ['https://pypi.python.org/simple/']


def projects_from_requirements(requirements):
    """Extract the project dependencies from a Requirements specification."""
    valid_reqs = []
    finder = PackageFinder(find_links=[], index_urls=index_urls)
    for requirements_path in requirements:
        reqs = parse_requirements(requirements_path, finder=finder)
        for req in reqs:
            if not req.name:
                continue
            elif req.editable:
                continue
            elif req.url and req.url.startswith('file:'):
                continue
            else:
                valid_reqs.append(req.name)
    return valid_reqs


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
            if url.scheme in ('http', 'https', 'file'):
                requirement = [sanitize_github_url(requirement, url)]
                try:
                    for project in projects_from_requirements(requirement):
                        projects[project] = None
                except:
                    raise ValidationError("Couldn't check %s." % requirement)
            else:
                projects[requirement] = None

        # from .jobs import get_all_projects
        # all_projects = get_all_projects(lower=True)
        # check_all_projects = len(all_projects) > 0

        self.projects = list(projects.keys())

        for index, project_name in enumerate(self.projects):
            validators.RegexValidator(project_name_re,
                                      'Project %s invalid' %
                                      project_name)(project_name)
            # if check_all_projects and project_name.lower() not in all_projects:
            #     self.projects[index] = '%s (not on PyPI)' % project_name
