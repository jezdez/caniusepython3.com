Stouts.apt
==========

[![Build Status](https://travis-ci.org/Stouts/Stouts.apt.png)](https://travis-ci.org/Stouts/Stouts.apt)

Ansible role apt which help you with:

* updating the apt-cache
* control if you want recommended packages
* control if you want suggested packages
* optionally add additional sources
* optionally install additional packages

#### Variables

```yaml
apt_enabled: yes              # Enable the role
apt_cache_valid_time: 3600    # Time (in seconds) the apt cache stays valid
apt_upgrade: no               # Perfoms aptupgrade. Values are (safe, full, dist)
apt_install_recommends: no    # Install the "recommended" packages
apt_install_suggests: no      # Install the "suggested" packages
apt_repositories: []          # List of sources which be added
apt_install_packages: no      # Install some utilities (see lise bellow)
apt_install_packages_list:    # List of packages which be installed
  - ack
  - command-not-found
  - curl
  - git
  - htop
  - iftop
  - iotop
  - mercurial
  - mosh
  - nmap
  - pciutils
  - screen
  - sysstat
  - vim
  - wget
```


#### Usage

Add `Stouts.apt` to your roles and set vars in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.apt

  vars:
    apt_install_recommends: yes
    apt_install_packages: yes
    apt_repositories:
      - ppa:fkrull/deadsnakes
```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.apt/issues)!
