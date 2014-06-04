Stouts.timezone
===============

[![Build Status](https://travis-ci.org/Stouts/Stouts.timezone.png)](https://travis-ci.org/Stouts/Stouts.timezone)

Ansible role which manage timezone (debian)

#### Variables
```yaml
timezone_enabled: yes                   # The role is enabled
timezone_timezone: UTC                  # Set timezone
```

#### Usage

Add `Stouts.timezone` to your roles and set vars in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.timezone

  vars:
    timezone_timezone: Europe/Moscow

```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.timezone/issues)!

