#!/usr/bin/python
#
# Copyright (C) 2013 Martin Owens
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Test the cron log extention with a test syslog example data file.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, '../')

import unittest
from crontab import CronTab
try:
    from test import test_support
except ImportError:
    from test import support as test_support


INITAL_TAB = """
* * * * * userscript &> /dev/null
* * * * * rootscript &> /dev/null
* * * * * shadowscript &> /dev/null
"""

class BasicTestCase(unittest.TestCase):
    """Test basic functionality of crontab."""
    def setUp(self):
        self.crontab = CronTab(tab=INITAL_TAB, log='test.log')

    def test_01_root(self):
        """Root's Log"""
        job = self.crontab.find_command('rootscript')[0]
        for log in job.log:
            print "ROOT: %s" % unicode(log)
        #ct = self.job.schedule(datetime(2009, 10, 11, 05, 12, 10))
        #self.assertTrue(ct)

    def test_02_user(self):
        """User's Log"""
        #ct = self.job.schedule(datetime(2000, 10, 11, 05, 12, 10))
        #self.assertEqual(ct.get_next(), datetime(2000, 10, 11, 06, 20, 0))

    def test_02_shadow(self):
        """Root's Shadow Log"""
        #ct = self.job.schedule(datetime(2001, 10, 11, 01, 12, 10))
        #self.assertEqual(ct.get_prev(), datetime(2001, 10, 10, 23, 20, 0))

if __name__ == '__main__':
    test_support.run_unittest(
       BasicTestCase,
    )
