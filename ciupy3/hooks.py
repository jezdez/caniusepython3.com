def run_raven(*args, **kwargs):
    """
    Set up raven for django by running a django command.
    It is necessary because chaussette doesn't run a django command.
    """
    from django.conf import settings
    from django.core.management import call_command
    if not settings.configured:
        settings.configure()

    call_command('validate')
    return True
