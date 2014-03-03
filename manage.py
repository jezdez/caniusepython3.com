#!/usr/bin/env python
import os
import sys

import envdir
from pathlib import Path

here = Path(__file__).parent
path = here / 'envs' / os.environ.get('ENVDIR', 'dev')
envdir.read(str(path))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ciupy3.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
