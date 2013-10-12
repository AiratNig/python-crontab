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
Test crontab interaction.
"""

import os
import sys

sys.path.insert(0, '../')

import unittest
from crontab import CronTab, py3
try:
    from test import test_support
except ImportError:
    from test import support as test_support

if py3:
    unicode = str

COMMANDS = [
    'firstcommand',
    'range',
    'byweek',
    'disabled',
    'spaced',
    'rebooted',
]

RESULT_TAB = """# First Comment
# Edit this line to test for mistaken checks

*/30 * * * * firstcommand
* 10-20/3 * * * range
# Middle Comment
* * * 10 * byweek # Comment One
# * * * * * disabled
0 5 * * * spaced # Comment  Two


@reboot rebooted
# Last Comment
"""

class BasicTestCase(unittest.TestCase):
    """Test basic functionality of crontab."""
    def setUp(self):
        self.crontab = CronTab(tabfile='data/test.tab')

    def test_00_root(self):
        """Not Root User"""
        self.assertFalse(self.crontab.root)

    def test_01_presevation(self):
        """All Entries Re-Rendered Correctly"""
        results = RESULT_TAB.split('\n')
        line_no = 0
        for line in self.crontab.lines:
            self.assertEqual(line, results[line_no])
            line_no += 1

    def test_02_access(self):
        """All Entries Are Accessable"""
        line_no = 0
        for cron in self.crontab:
            self.assertEqual(str(cron.command), COMMANDS[line_no])
            line_no += 1

    def test_03_blank(self):
        """Render Blank"""
        job = self.crontab.new(command='blank')
        self.assertEqual(job.render(), '* * * * * blank')

    def test_04_number(self):
        """Render Number"""
        job = self.crontab.new(command='number')
        job.minute.on(4)
        self.assertEqual(job.render(), '4 * * * * number')

    def test_05_fields(self):
        """Render Hours Days and Weeks"""
        job = self.crontab.new(command='fields')
        job.hour.on(4)
        self.assertEqual(job.render(), '* 4 * * * fields')
        job.dom.on(5)
        self.assertEqual(job.render(), '* 4 5 * * fields')
        job.month.on(6)
        self.assertEqual(job.render(), '* 4 5 6 * fields')
        job.dow.on(7)
        self.assertEqual(job.render(), '* 4 5 6 7 fields')

    def test_06_clear(self):
        """Render Hours Days and Weeks"""
        job = self.crontab.new(command='clear')
        job.minute.on(3)
        job.hour.on(4)
        job.dom.on(5)
        job.month.on(6)
        job.dow.on(7)
        self.assertEqual(job.render(), '3 4 5 6 7 clear')
        job.clear()
        self.assertEqual(job.render(), '* * * * * clear')

    def test_07_range(self):
        """Render Time Ranges"""
        job = self.crontab.new(command='range')
        job.minute.during(4,10)
        self.assertEqual(job.render(), '4-10 * * * * range')
        job.minute.during(15,19)
        self.assertEqual(job.render(), '15-19 * * * * range')
        job.minute.clear()
        self.assertEqual(job.render(), '* * * * * range')
        job.minute.during(15,19)
        self.assertEqual(job.render(), '15-19 * * * * range')
        job.minute.also.during(4,10)
        self.assertEqual(job.render(), '4-10,15-19 * * * * range')

    def test_08_sequence(self):
        """Render Time Sequences""" 
        job = self.crontab.new(command='seq')
        job.hour.every(4)
        self.assertEqual(job.render(), '* */4 * * * seq')
        job.hour.during(2, 10)
        self.assertEqual(job.render(), '* 2-10 * * * seq')
        job.hour.clear()
        self.assertEqual(job.render(), '* * * * * seq')
        job.hour.during(2, 10).every(4)
        self.assertEqual(job.render(), '* 2-10/4 * * * seq')
        job.hour.also.during(1, 4)
        self.assertEqual(job.render(), '* 1-4,2-10/4 * * * seq')

    def test_10_comment(self):
        """Render cron Comments"""
        job = self.crontab.new(command='com', comment='I love this')
        self.assertEqual(unicode(job), '* * * * * com # I love this')

    def test_11_disabled(self):
        """Disabled Job"""
        jobs = self.crontab.find_command('firstcommand')
        self.assertTrue(jobs[0].enabled)
        jobs = self.crontab.find_command('disabled')
        self.assertFalse(jobs[0].enabled)

    def test_12_disable(self):
        """Disable and Enable Job"""
        job = self.crontab.new(command='dis')
        job.enable(False)
        self.assertEqual(unicode(job), '# * * * * * dis')
        job.enable()
        self.assertEqual(unicode(job), '* * * * * dis')

    def test_20_write(self):
        """Write CronTab to file"""
        self.crontab.write('output.tab')
        self.assertTrue(os.path.exists('output.tab'))
        os.unlink('output.tab')

    def test_21_multiuse(self):
        """Multiple Renderings"""
        cron = '# start of tab'
        for i in range(10):
            crontab = CronTab(tab=cron)
            job = crontab.new(command='multi')
            cron = unicode(crontab)
            crontab = CronTab(tab=cron)
            crontab.find_command('multi')[0].delete()
            cron = unicode(crontab)
        self.assertEqual(unicode(crontab), '# start of tab\n')

    def test_22_min(self):
        """Minimum Field Values"""
        job = self.crontab.new(command='min')
        job.minute.on('<')
        job.hour.on('<')
        job.dom.on('<')
        job.month.on('<')
        self.assertEqual(unicode(job), '@yearly min')

    def test_23_max(self):
        """Maximum Field Values"""
        job = self.crontab.new(command='max')
        job.minute.on('>')
        job.hour.on('>')
        job.dom.on('>')
        job.month.on('>')
        self.assertEqual(unicode(job), '59 23 31 12 * max')

    def test_24_specials(self):
        """Specials Conversion"""
        tab = CronTab(tabfile='data/specials.tab')
        self.assertEqual(tab.render(), """@hourly hourly\n@midnight daily\n@weekly weekly\n""")

if __name__ == '__main__':
    test_support.run_unittest(
       BasicTestCase,
    )
