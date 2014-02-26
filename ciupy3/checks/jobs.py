import uuid
from urlparse import urlparse
from collections import OrderedDict

from pq.decorators import job
from redis_cache import get_redis_connection

from caniusepython3.__main__ import (projects_from_requirements,
                                     message, pprint_blockers)
from caniusepython3 import blocking_dependencies, all_py3_projects


redis = get_redis_connection('default')

TROVE_KEY_NAME = 'trove_classifiers_key'


def compatible_projects():
    key_name = redis.get(TROVE_KEY_NAME)
    return redis.smembers(key_name)


@job('default')
def fetch_trove_classifiers():
    with redis.lock('fetch_trove_classifiers'):
        # try to get the old fetch id first
        old_key_name = redis.get(TROVE_KEY_NAME)

        # then populate a set of Python 3 projects in Redis
        new_key_name = uuid.uuid4()
        projects = all_py3_projects()
        for project in projects:
            redis.sadd(new_key_name, project)
        redis.set(TROVE_KEY_NAME, new_key_name)

        # get rid of the old fetch set if needed
        if old_key_name is not None:
            redis.delete(old_key_name)

        # return number of Python 3 projects
        count = len(projects)
        redis.set('compatible_count', count)
        return count


@job('default')
def run_check(requirements):
    split_requirements = requirements.splitlines()

    projects = OrderedDict()

    for split_requirement in split_requirements:
        parsed_url_requirement = urlparse(split_requirement)
        if parsed_url_requirement.scheme in ('http', 'https'):
            try:
                for project in projects_from_requirements(split_requirement):
                    projects[project] = split_requirement
            except:
                continue
        else:
            projects[project] = split_requirement

    blockers = blocking_dependencies(projects.keys(), compatible_projects())
    result = list(message(blockers)) + pprint_blockers(blockers)

    return '\n'.join(result)
