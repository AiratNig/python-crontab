#!/usr/bin/python

import sys
sys.path.append('../')

import crontab
from crontab import CronTab

t = CronTab()

for slice in t:
	print slice

