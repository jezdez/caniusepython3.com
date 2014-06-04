Stouts.deploy
=============

[![Build Status](https://travis-ci.org/Stouts/Stouts.deploy.png)](https://travis-ci.org/Stouts/Stouts.deploy)

Ansible role which creates deploy directories and sets deploy variables, also ensures for deploy user exists
The Boilerplate for using in playbooks and other roles.


#### Variables

The role variables and default values.

```yaml
deploy_enabled: yes                           # Enable the role

deploy_env: develop                           # Pick environment variable

deploy_user: "{{ansible_ssh_user}}"           # Set deploy user
deploy_group: "{{deploy_user}}"               # Set deploy group

deploy_app_name: web                          # Set application name

deploy_dir: /usr/lib/{{deploy_app_name}}      # Root deploy directory
deploy_etc_dir: "{{deploy_dir}}/etc"          # Directory where placed configuration files
deploy_log_dir: "{{deploy_dir}}/log"          # Directory where placed logs
deploy_run_dir: "{{deploy_dir}}/run"          # Directory where placed unix sockets and pid files
deploy_src_dir: "{{deploy_dir}}/src"          # Source's directory
deploy_bin_dir: "{{deploy_dir}}/bin"          # Directory where placed scripts

deploy_dir_skip: ["{{deploy_src_dir}}", "{{deploy_bin_dir}}"]       # Dont create this dirs, only keep variables
```

#### Usage

Add `Stouts.deploy` to your roles and set variables in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.deploy

  vars:
    deploy_app_name: facebook  # ;)
    deploy_user: deploy
```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.deploy/issues)!
