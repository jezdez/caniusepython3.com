Stouts.hostname
===============

[![Build Status](https://travis-ci.org/Stouts/Stouts.hostname.png)](https://travis-ci.org/Stouts/Stouts.hostname)

Ansible role for manage the hostname

#### Variables

THe role variables and default values.

```yaml
hostname_enabled: yes                       # Enable module
hostname_hostname: "{{inventory_hostname}}" # Set hostname
hostname_hostname_short: "{{hostname_hostname.split('.')[:-1]|join('.')}}" # Set short hostname
```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.hostname/issues)!
