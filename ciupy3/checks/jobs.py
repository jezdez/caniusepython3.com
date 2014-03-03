import uuid
from django.utils.timezone import now

from pq.decorators import job
from caniusepython3 import blocking_dependencies, all_py3_projects

from .models import Check, get_redis

TROVE_KEY_NAME = 'trove_classifiers_key'
COUNT_KEY = 'compatible_count'


@job('default')
def fetch_all_py3_projects():
    """
    A job to be run periodically (e.g. daily) to update the
    Python 3 compatible projects from PyPI.
    """
    redis = get_redis()
    with redis.lock('fetch_trove_classifiers'):
        # try to get the old fetch id first
        old_key_name = redis.get(TROVE_KEY_NAME)

        # then populate a set of Python 3 projects in Redis
        new_key_name = uuid.uuid4().hex
        projects = all_py3_projects()
        for project in projects:
            redis.sadd(new_key_name, str(project))
        redis.set(TROVE_KEY_NAME, new_key_name)

        # get rid of the old fetch set if needed
        if old_key_name is not None:
            redis.delete(old_key_name)

        # return number of Python 3 projects
        compatible_count = len(projects)
        redis.set(COUNT_KEY, compatible_count)
        return compatible_count


def get_compatible():
    redis = get_redis()
    return redis.get(COUNT_KEY) or None


def get_all_py3_projects():
    """
    Return the list of projects compatible to Python 3 according
    to PyPI
    """
    redis = get_redis()
    key_name = redis.get(TROVE_KEY_NAME)
    return {project.decode('utf-8')
            for project in redis.smembers(key_name)}


def get_or_fetch_all_py3_projects():
    """
    Get the compatible projets stored in redis and if not available
    try to fetch it synchronysly, then fail if that errors as well.
    """
    projects = get_all_py3_projects()
    if not projects:
        fetch_all_py3_projects()
        projects = get_all_py3_projects()
        if not projects:
            raise ValueError('Something went wrong while fetching '
                             'the Python 3 projects from PyPI')
    return projects


@job('default')
def run_check(pk):
    """
    The central job to run the check. Called after a check has been
    created.
    """
    check = Check.objects.get(pk=pk)
    check.started_at = now()

    all_py3_projects = get_or_fetch_all_py3_projects()
    blockers = blocking_dependencies(check.projects, all_py3_projects)
    blockers_mapping = {}
    for blocker in sorted(blockers, key=lambda x: tuple(reversed(x))):
        blockers_mapping[blocker[0]] = blocker[1:]
    check.blockers = blockers_mapping

    flattened_blockers = set()
    for blocker_reasons in blockers:
        for blocker in blocker_reasons:
            flattened_blockers.add(blocker)
    check.unblocked = len(flattened_blockers)

    check.finished_at = now()
    check.save()

    return blockers
