Stouts.source
=============

[![Build Status](https://travis-ci.org/Stouts/Stouts.source.png)](https://travis-ci.org/Stouts/Stouts.source)

Ansible role wich manage source code from git or mercurial repositoires

#### Variables
```yaml
source_enabled: yes                   # Enable role
source_sources: []                    # Repositories to clone
source_sources_type: git              # Set repository type (git, hg)
source_copy_keys: []                  # Copy defined key files from host to server in ~/.ssh/*
source_reload_cmd: ":"                # Run the shell command when source has benn changed

source_user: "{{ansible_ssh_user}}"   # Run from user
source_group: "{{source_user}}"       # Run from user
source_user_ssh_home: ~{{source_user}}/.ssh

# Repository defaults (could be replaced individually)
source_default_dest: ""               # Default destination
source_default_force: yes             # Default force
source_default_accept_hostkey: yes    # Accept hostkey (git)
source_default_bare: no               # Clone bare by default (git)
source_default_key_file: ""           # Default key file (git)
source_default_recursive: yes         # Clone recursivly by default (git)
source_default_remote: origin         # Default remote name (git)
source_default_ssh_opts:              # Default ssh options (git)
source_default_version: HEAD          # Default version (branch, tag, commit) (git)
source_default_revision: default      # Default revision (branch, tag, commit) (hg)
source_default_purge: no              # Default purge (hg)

source_fingerprints:
   - "bitbucket.org,131.103.20.167 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAubiN81eDcafrgMeLzaFPsw2kNvEcqTKl/VqLat/MaB33pZy0y3rJZtnqwR2qOOvbwKZYKiEO1O6VqNEBxKvJJelCq0dTXWT5pbO2gDXC6h6QDXCaHo6pOHGPUy+YBaGQRGuSusMEASYiWunYN0vCAI8QaXnWMXNMdFP3jHAJH0eDsoiGnLPBlBp4TNm6rYI74nMzgz3B9IikW4WVK+dc8KZJZWYjAuORU3jc1c/NPskD2ASinf8v3xnfXeukU0sJ5N6m5E8VLjObPEO+mN2t/FZTMZLiFqPWc/ALSqnMnnhwrNi2rbfg/rd/IpL8Le3pSBne8+seeFVBoGqzHM9yXw=="
   - "github.com,204.232.175.90 ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ=="
```

#### Usage

Add `Stouts.source` to your roles and set vars in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.source

  vars:
    source_copy_keys:
      - "{{inventory_dir}}/keys/deploy_key"
    source_sources:
      - repo: https://github.com/Dipsomaniac/dj-simple.git
        dest: /usr/lib/simple/source
        key_file: "/home/{{ansible_ssh_user}}/.ssh/deploy_key"
        version: "develop"
    source_reload_cmd: reload uwsgi
```

See [git-module](http://docs.ansible.com/git_module.html) and [hg-module](http://docs.ansible.com/hg_module.html) for source params.

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.source/issues)!
