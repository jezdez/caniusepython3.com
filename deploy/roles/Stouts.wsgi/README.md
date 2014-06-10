Stouts.wsgi
===========

[![Build Status](https://travis-ci.org/Stouts/Stouts.wsgi.png)](https://travis-ci.org/Stouts/Stouts.wsgi)

Ansible role which deploys wsgi application (uwsgi, nginx, virtualenv)

* Install and setup nginx, uwsgi;
* Setup and manage project requirements and virtualenv;
* Deploy project with uwsgi, enable monitoring;


#### Requirements & Dependencies

- [Stouts.deploy](https://github.com/Stouts/Stouts.deploy)
- [Stouts.python](https://github.com/Stouts/Stouts.python)
- [Stouts.nginx](https://github.com/Stouts/Stouts.nginx)


#### Variables

The role variables and default values.

```yaml
wsgi_enabled: yes                                     # Enable the role

wsgi_app_name: "{{deploy_app_name}}"
wsgi_user: "{{deploy_user}}"
wsgi_group: "{{deploy_group}}"
wsgi_deb_packages: []                                 # Additional deb packages which will be installed
wsgi_pip_packages: []                                 # Additional pip packages which will be installed

# Directories
wsgi_src_dir: "{{deploy_src_dir}}"
wsgi_run_dir: "{{deploy_run_dir}}"
wsgi_etc_dir: "{{deploy_etc_dir}}"
wsgi_log_dir: "{{deploy_log_dir}}"

# Application options
wsgi_app: "{{wsgi_src_dir}}/wsgi.py"                  # File contains wsgi application
wsgi_pip_requirements: >                              # Python requirements file (set blank "" to disable install)
  "{{wsgi_src_dir}}/requirements.txt"
wsgi_env_dir: "{{deploy_dir}}/env"                    # Setup app to virtualenv (set blank "" to disable)
wsgi_env_python: python                               # Virtualenv python interpreter

# UWSGI options
wsgi_uwsgi_ini: "{{wsgi_etc_dir}}/uwsgi.ini"
wsgi_uwsgi_socket: "{{wsgi_run_dir}}/uwsgi.sock"
wsgi_uwsgi_reload: no
wsgi_uwsgi_processes: 4
wsgi_uwsgi_enable_threads: no
wsgi_uwsgi_max_requests: 2000
wsgi_uwsgi_no_orphans: yes
wsgi_uwsgi_options: []

# Nginx options
wsgi_nginx_servernames: "{{inventory_hostname}}"      # Listen servernames (separated by space)
wsgi_nginx_redirect_www: no                           # Redirect www.servername to servername
wsgi_nginx_port: 80                                   # Listen port
wsgi_nginx_ini: "{{wsgi_etc_dir}}/nginx.conf"
wsgi_nginx_static_locations: [/static/, /media/]
wsgi_nginx_options: []

# Logging options
wsgi_log_rotate: yes                                   # Rotate wsgi logs.
wsgi_log_rotate_options:
  - "create 644 {{wsgi_user}} {{wsgi_group}}"
  - compress
  - copytruncate
  - daily
  - dateext
  - rotate 7
  - size 10M
```

#### Usage

Clone dependencies.
Add `Stouts.wsgi` to your roles and change variables in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.wsgi

  vars:
    wsgi_nginx_servernames: facebook.com
```

#### License

Licensed under the MIT License. See the LICENSE file for details.


#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.wsgi/issues)!
