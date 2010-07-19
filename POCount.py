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

# type              strings      words (source)    words (translation)
# translated:     788 (100%)       3352 (100%)            3555
# fuzzy:            0 (  0%)          0 (  0%)             n/a
# untranslated:     0 (  0%)          0 (  0%)             n/a
# Total:          788              3352                   3555

# Filename, Translated Messages, Translated Source Words, Translated Target Words, Fuzzy Messages, Fuzzy Source Words, Untranslated Messages, Untranslated Source Words, Total Message, Total Source Words, Review Messages, Review Source Words
# el.po,  788, 3352, 3555, 0, 0, 0, 0, 788, 3352

class POCount:
    def __init__(self):
        self.patTranslated = re.compile(u"^[^,].*,\s+\w+,\s+(?P<translated>\w+)", re.UNICODE)
        self.stats = {}

    def parse(self, filepath):
        self.process = subprocess.Popen(['/usr/bin/pocount', '--csv', filepath], shell=False, stdout=subprocess.PIPE)
        self.output = self.process.communicate()[0]
        self.outputlines = re.split("\n", self.output)

        self.line = self.outputlines[1]
        self.m = self.patTranslated.match(self.line)
        self.stats['translated'] = self.m.group('translated')

        return self.stats

    def getPOCountStats(self):
      return self.stats

if __name__ == '__main__':
      a = POCount()
      print a.parse('/tmp/file1.po')

