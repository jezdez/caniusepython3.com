## Ansibles - tmpreaper [![Build Status](https://travis-ci.org/Ansibles/tmpreaper.png)](https://travis-ci.org/Ansibles/tmpreaper)

Ansible role which installs and configures tmpreaper.


#### Requirements & Dependencies
- Tested on Ansible 1.4 or higher.


#### Variables

```yaml
tmpreaper_show_warning: false
tmpreaper_time: 7d
tmpreaper_protect_extra: /tmp/*.sock /tmp/hsperfdata_*
tmpreaper_dirs: /tmp/. /var/tmp/.
tmpreaper_delay: 256
tmpreaper_additional_options: --all
tmpreaper_cron_hour: 2
tmpreaper_cron_minute: 15
```


#### License

Licensed under the MIT License. See the LICENSE file for details.


#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/ansibles/tmpreaper/issues)!
