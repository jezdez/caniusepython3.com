from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

import redis_lock

from ciupy3.checks.models import Project, get_redis


class Command(BaseCommand):
    help = "Checks all projects for updates"
    requires_model_validation = False

    def handle(self, **options):
        redis = get_redis()
        lock = redis_lock.Lock(redis, "check_all_projects", expire=60 * 60 * 2)

        acquired = False
        try:
            acquired = lock.acquire(blocking=False)
            if acquired:
                projects = Project.objects.all()
                count = projects.count()
                for i, project in enumerate(projects, 1):
                    self.stdout.write('Checking (%s/%s): %s' %
                                      (i, count, project))
                    try:
                        project.run_check(delay=False)
                    except ValidationError:
                        continue
        finally:
            if acquired:
                lock.release()
