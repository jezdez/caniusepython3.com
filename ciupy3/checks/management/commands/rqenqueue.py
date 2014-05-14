from django.core.management.base import BaseCommand
from optparse import make_option

import django_rq


class Command(BaseCommand):
    help = "Queue a function now."
    args = "<function arg arg ...>"

    option_list = BaseCommand.option_list + (
        make_option('--queue', '-q', dest='queue', default='',
            help='Specify the queue [default]'),
        make_option('--timeout', '-t', type="int", dest='timeout',
            help="A timeout in seconds"),
    )

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        verbosity = int(options.get('verbosity', 1))
        timeout = options.get('timeout')
        queue = options.get('queue')
        queue = queue or 'default'
        q = django_rq.get_queue(queue)
        job = q.enqueue_call(args[0], args=args[1:], timeout=timeout)
        if verbosity:
            print('Job %s created' % job.id)
