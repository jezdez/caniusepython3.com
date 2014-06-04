Stouts.locale
=============

[![Build Status](https://travis-ci.org/Stouts/Stouts.locale.png)](https://travis-ci.org/Stouts/Stouts.locale)

Ansible role which ensure the defined locales are exists.

#### Variables

```yaml
locale_enabled: yes        # Enable role
locale_locales:            # List of locales to installed
  - en_US.UTF-8
```

#### Usage

Add `Stouts.locale` to your roles and set `locale_locales` in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.locale

  vars:
    locale_locales:
      - en_US.UTF-8
      - ru_RU.UTF-8

```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.locale/issues)!
