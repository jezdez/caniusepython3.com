Stouts.wal-e
============

[![Build Status](https://travis-ci.org/Stouts/Stouts.wale.png)](https://travis-ci.org/Stouts/Stouts.wale)

Ansible role which performs continuous archiving of PostgreSQL WAL files

* Install and setup [Wal-e](https://github.com/wal-e/wal-e)
* Setup cronjobs

#### Variables

The role variables and default values.

```yaml
wale_enabled: yes                     # The role is enabled
wale_home: /etc/wale                  # Where make runscript
wale_logdir: /var/log/wale            # Where store logs
wale_user: "postgres"
wale_group: "postgres"
wale_cron: []                          # Setup cronjobs
                                       # Ex. wale_cron:
                                       #     - { schedule: 0 2 * * *, cmd: backup-push /var/lib/postgresql/9.1/main/ }

# Set the credentials for enable upload to AWS S3
wale_aws_access_key_id:               
wale_aws_secret_access_key:
wale_aws_s3_prefix:

# Set the credentials for enable upload to WABS
wale_wabs_account_name:               
wale_wabs_access_key:
wale_wabs_prefix:

# Set the credentials for enable upload to SWIFT
wale_swift_authurl:
wale_swift_tenant:
wale_swift_user:
wale_swift_password:
wale_swift_prefix:
```

#### Usage

Add `Stouts.wale` to your roles and change variables in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Ansibles.postgresql
    - Stouts.wsgi

  vars:
    postgresql_wal_level: hot_standby
    postgresql_archive_mode: yes
    postgresql_archive_command: /etc/wale/wale.sh wal-push %p
    postgresql_archive_timeout: 60

# Stouts.wale
# ===========
    wale_aws_access_key_id: <access_key>
    wale_aws_secret_access_key: <secret_key>
    wale_aws_s3_prefix: s3://<bucket>/{{inventory_hostname}}
    wale_cron:
      - { schedule: "0 2 * * *", cmd: "backup-push /var/lib/postgresql/{{postgresql_version}}/main" }

```

#### License

Licensed under the MIT License. See the LICENSE file for details.


#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/Stouts/Stouts.wale/issues)!
