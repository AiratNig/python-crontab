#!/usr/bin/python
#
# Copyright (C) 2009 Martin Owens
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
Test crontab interaction.
"""

import os
import sys

import unittest
from test import test_support
from crontab import CronTab

INITAL_TAB = """
# First Comment
*/30 * * * * firstcommand
# Middle Comment
* * * 10 * byweek
 00 5  *   *   *      spaced
@reboot rebooted
# Last Comment"""

COMMANDS = [
    'firstcommand',
    'byweek',
    'spaced',
    'rebooted',
]

RESULT_TAB = """
# First Comment
*/30 * * * * firstcommand
# Middle Comment
* * * 10 * byweek
0 5 * * * spaced
@reboot rebooted
# Last Comment
"""

class BasicTestCase(unittest.TestCase):
    """Test basic functionality of crontab."""
    def setUp(self):
        self.crontab = CronTab(fake_tab=INITAL_TAB)

    def test_presevation(self):
        """All Entries Re-Rendered Correctly"""
        self.assertEqual(self.crontab.fake, INITAL_TAB,
            "Inital values are set currently")
        self.crontab.write()
        results = RESULT_TAB.split('\n')
        line_no = 0
        for line in self.crontab.fake.split('\n'):
            self.assertEqual(line, results[line_no])
            line_no += 1

    def test_access(self):
        """All Entries Are Accessable"""
        line_no = 0
        for cron in self.crontab:
            self.assertEqual(unicode(cron.command), COMMANDS[line_no])
            line_no += 1

if __name__ == '__main__':
    test_support.run_unittest(
       BasicTestCase,
    )
