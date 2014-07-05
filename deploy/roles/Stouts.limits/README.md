Stouts.limits
=============

[![Build Status](https://travis-ci.org/Stouts/Stouts.locale.png)](https://travis-ci.org/Stouts/Stouts.locale)

Ansible role which manage system limis.

#### Variables

```yaml
limits_enabled: yes
limits_path: /etc/security/limits.d/tune.conf

# See http://linux.die.net/man/5/limits.conf for description
limits_limits:
  - *    -    nofile    65535

limits_sysctl:
  - { name: 'net.ipv4.tcp_tw_recycle',      value: '1' }
  - { name: 'net.ipv4.tcp_tw_reuse',        value: '1' }
  - { name: 'net.ipv4.ip_local_port_range', value: '15000 35530' }
```

#### Usage

Add `Stouts.limits` to your roles and set vars in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.limits

  vars:
    limits_limits:
    - *    -    nofile    200000
```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.limits/issues)!
