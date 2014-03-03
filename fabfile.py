import glob
from fabric.api import *  # noqa
from fabric.contrib.files import append
from gitric.api import *  # noqa
from pathlib import Path
from contextlib import contextmanager

env.hosts = ['jezdez@jezdez.com']

env.projectname = 'ciupy3'
env.appname = 'ciupy3'
env.remote = 'origin'
env.user = 'jezdez'
env.home = '/home/{user}'.format(**env)
env.codedir = '{home}/webapps/{projectname}'.format(**env)
env.venv = '{home}/.virtualenvs/{appname}'.format(**env)


@contextmanager
def virtualenv():
    with path(env.venv + '/bin', 'prepend'):
        yield


@task
def deploy(commit=None):
    git_seed(env.codedir, commit)
    # stop your service here
    supervisor('stop jezdez_web')
    git_reset(env.codedir, commit)
    with virtualenv():
        with cd(env.codedir):
            run('pip install --pre -r requirements.txt')
            run('./manage.py collectstatic --noinput --configuration=Prod')
    # restart your service here
    supervisor('start jezdez_web')


@task
def pushprodconfig():
    run('mkdir -p {}/envs/prod'.format(env.codedir))
    for path in glob.glob('./envs/prod/*'):
        path = Path(path)
        name = Path(env.codedir, 'envs', 'prod', path.name)
        with path.open() as envfile:
            append(name, envfile.read())


@task
def supervisor(command):
    with cd(env.home):
        run('supervisorctl {}'.format(command))


@task
def upgrade():
    local('pip install -r requirements.txt')


@task
def dev():
    local('foreman start')


@task
def migrate():
    local('python manage.py syncdb --noinput')
    local('python manage.py migrate')
