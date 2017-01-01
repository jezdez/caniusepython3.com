import uuid
from xmlrpc.client import ServerProxy

from django.db.models import F, Sum
from django.utils.timezone import now

from celery import shared_task

from caniusepython3 import dependencies

from .models import Check, Project, get_redis

TROVE_KEY_NAME = 'trove_classifiers_key'
TROVE_COUNT_KEY = 'compatible_count'
ALL_KEY_NAME = 'all_key'
ALL_COUNT_KEY = 'all_count'
CHECKED_COUNT_KEY = 'checked_count'
OVERRIDE_KEY = 'override'
OVERRIDE_URL = ('https://raw.github.com/brettcannon/caniusepython3/'
                'master/caniusepython3/overrides.json')


def all_projects():
    client = ServerProxy('https://pypi.python.org/pypi')
    return client.list_packages()


@shared_task
def fetch_all_projects():
    """
    A job to be run periodically (e.g. daily) to update the projects from PyPI.
    """
    redis = get_redis()
    # try to get the old fetch id first
    old_key_name = redis.get(ALL_KEY_NAME)

    # then populate a set of Python 3 projects in Redis
    new_key_name = uuid.uuid4().hex
    projects = all_projects()
    pipeline = redis.pipeline()
    for project in projects:
        pipeline.sadd(new_key_name, str(project))
    pipeline.set(ALL_KEY_NAME, new_key_name)

    # get rid of the old fetch set if needed
    if old_key_name is not None:
        pipeline.delete(old_key_name)

    # return number of Python 3 projects
    compatible_count = len(projects)
    pipeline.set(ALL_COUNT_KEY, compatible_count)
    pipeline.execute()
    return compatible_count


def get_compatible():
    redis = get_redis()
    return redis.get(TROVE_COUNT_KEY) or None


def get_total():
    redis = get_redis()
    return redis.get(ALL_COUNT_KEY) or None


def get_checked():
    redis = get_redis()
    return redis.get(CHECKED_COUNT_KEY) or None


def decode_name(name, lower=False):
    name = name.decode('utf-8')
    if lower:
        return name.lower()
    else:
        return name


def handle_projects(project_list, lower):
    projects = {}
    for project in project_list:
        decoded_project = decode_name(project)
        lower_decoded_project = decoded_project.lower()
        if lower:
            decoded_project = lower_decoded_project
        projects[decoded_project] = lower_decoded_project
    return projects


def get_all_projects(lower=False):
    """
    Return the list of all projects on PyPI
    """
    redis = get_redis()
    key_name = redis.get(ALL_KEY_NAME)
    return handle_projects(redis.smembers(key_name), lower)


def get_or_fetch_all_projects(lower=False):
    """
    Get all projects stored in redis and if not available
    try to fetch it synchronysly, then fail if that errors as well.
    """
    projects = get_all_projects(lower)
    if not projects:
        fetch_all_projects()
        projects = get_all_projects(lower)
        if not projects:
            raise ValueError('Something went wrong while fetching '
                             'all projects from PyPI')
    return projects


@shared_task(time_limit=60)
def run_check(pk):
    """
    The central job to run the check. Called after a check has been
    created.
    """

    check = Check.objects.get(pk=pk)
    started_at = now()

    blockers = dependencies.blockers(check.projects)
    blockers_mapping = {
        blocker: path
        for [blocker, *path]
        in sorted(blockers, key=lambda x: tuple(reversed(x)))
    }

    flattened_blockers = {
        blocker
        for blocker_reasons in blockers
        for blocker in blocker_reasons
    }

    Check.objects.filter(pk=pk).update(
        started_at=started_at,
        finished_at=now(),
        blockers=blockers_mapping,
        unblocked=len(flattened_blockers),
        runs=F('runs') + 1
    )


@shared_task
def update_checked_count():
    redis = get_redis()
    # the number of "publicly" announced checks is the sum of all runs
    # and the number of projects that have been created lazily
    public_checks = (Check.objects.filter(public=True)
                                  .aggregate(Sum('runs')))
    project_count = Project.objects.count()
    redis.set(CHECKED_COUNT_KEY,
              public_checks.get('runs__sum') or 0 + project_count)


def real_project_name(value):
    all_projects = get_or_fetch_all_projects()
    all_projects_flipped = dict((value, key)
                                for key, value in all_projects.items())
    return all_projects_flipped.get(value.lower(), None)


@shared_task
def fill_autocomplete_index():
    projects = get_or_fetch_all_projects()
    redis = get_redis()
    with redis.pipeline() as pipe:
        for project_name, project_label in projects.items():
            value = '%s:%s' % (project_label, project_name)
            pipe.zadd('autocomplete', 0, value)
        pipe.execute()
