#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

# Author  : Simos Xenitellis <simos@gnome.org>, 2010

PROGNAME='gnome-l10n-translator-stats'

PACKAGE_NAME    = 'GNOME L10n Translator Stats'
PACKAGE_VERSION = '0.1'
PACKAGE_AUTHORS = ['Simos Xenitellis <simos@gnome.org>']
PACKAGE_COPYRIGHT = 'Copyright 2010 Simos Xenitellis'

import subprocess
import re
import sys

# *** Statistics
#Changed translations:     2
#New fuzzy translations:   0
#Lost translations:        0
#New translations:        92
#Removed messages:       809
#New messages:            93

class PODiff:
    def __init__(self):
        self.patChanged = re.compile(u"^Changed translations:\s+(?P<changed>\w+)", re.UNICODE)
        self.stats = {}

    def parse(self, filepath1, filepath2):
        self.process = subprocess.Popen(['/usr/local/bin/podiff', filepath1, filepath2], shell=False, stdout=subprocess.PIPE)
        self.output = self.process.communicate()[0]
        self.outputlines = re.split("\n", self.output)

        self.line = self.outputlines[1]
        self.m = self.patChanged.match(self.line)
        self.stats['changed'] = self.m.group('changed')

        return self.stats

    def getPODiffStats(self):
      return self.stats

if __name__ == '__main__':
      a = PODiff()
      print a.parse('/tmp/file1.po', '/tmp/file2.po')

