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
os.environ['COMPATIBILITY'] = 'True'

sys.path.insert(0, '../')

import unittest
from test import test_support
from crontab import CronTab

INITAL_TAB = """
# First Comment
*/30 * * * * firstcommand
"""

class BasicTestCase(unittest.TestCase):
    """Test basic functionality of crontab."""
    def setUp(self):
        self.crontab = CronTab(fake_tab=INITAL_TAB)

    def test_03_addition(self):
        """New Job Rendering"""
        job = self.crontab.new(command='addition1')

        job.minute().during(4, 9)
        job.hour().during(2, 10).every(2)
        job.dom().every(10)

        self.assertNotEqual(job.render(), '4-9 2-10/2 */3 * * addition1')
        self.assertEqual(job.render(), '4,5,6,7,8,9 2,4,6,8,10 1,11,21,31 * * addition1')


if __name__ == '__main__':
    test_support.run_unittest(
       BasicTestCase,
    )
