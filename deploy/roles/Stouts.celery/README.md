Stouts.celery
=============

[![Build Status](https://travis-ci.org/Stouts/Stouts.celery.png)](https://travis-ci.org/Stouts/Stouts.celery)

Ansible role whith manage [Celery](http://celery.readthedocs.org/en/latest/index.html)

Is under development.

#### Requirements & Dependencies

The role doesnt have any requirements, but [Stouts.deploy](https://github.com/Stouts/Stouts.deploy) is recomended.


#### Variables

```yaml
celery_enabled: yes                                   # The role is enabled
celery_remove: no                                     # Uninstall the role

celery_app_name: "{{deploy_app_name|default('web')}}" # Application name
celery_bin: celery                                    # Celery executable. Ex:
                                                      # celery_bin: /path/to/virtualenv/bin/celery
                                                      # celery_bin: "python /path/to/django/manage.py celery --settings=settings"
                                                      # celery_bin: "/path/to/virtualenv/python /path/to/django/manage.py celery --settings=settings"
                  

celery_run:                                           # Start celery. See default values below. Ex:
- { action: worker }                                  # - { action: worker, queue: 'hard', concurrency: 4, loglevel: debug, user=deploy }
- { action: beat }                                    # - { action: beat, loglevel: debug }
                                                      # - { action: worker, opts: '--settings=settings.local' }

celery_concurrency: 1                                 # Set default concurence level
celery_user: "{{deploy_user|default('root')}}"        # Set default user
celery_app_dir: "{{deploy_src_dir|default('/usr/lib/' + celery_app_name)}}" # Set default application directory
celery_app_module: "{{celery_app_name}}"              # Set default application module
celery_log_dir: "{{deploy_log_dir|default(celery_app_dir + '/log')}}" # Set default log directory
celery_log_level: info                                # Set default log level
celery_log_rotate: yes                                # Enable log rotation
celery_opts:                                          # Set additional options
```

#### Usage

* Add `Stouts.celery` to your roles
* Setup the role variables in your playbook file if needed

Example:

```yaml

- hosts: all

  roles:
    - Stouts.celery

  vars:
    celery_bin: "{{wsgi_env_dir}}/bin/celery"
    celery_app_module: "{{deploy_app_name}}.main"
```

#### License

Licensed under the MIT License. See the LICENSE file for details.


#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.celery/issues)!
