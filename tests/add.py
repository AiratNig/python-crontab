#!/usr/bin/python

import sys
sys.path.append('../')

from crontab import CronTab

tab = CronTab()
tab.new(command="/foo/bar")
tab.write()

