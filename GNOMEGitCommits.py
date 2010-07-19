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

class GNOMEGitCommits:
    def __init__(self):
        self.patHash = re.compile(u"^commit (?P<hash>\w+)", re.UNICODE)
        self.patAuthor = re.compile(u"^Author: (?P<author>.*)", re.UNICODE)
        self.patDate = re.compile(u"^Date:\s+(?P<date>.*)", re.UNICODE)
        self.patMerge = re.compile(u"^Merge:.*", re.UNICODE)
        self.patEmpty = re.compile(u"^[\s\t]*$", re.UNICODE)
        self.patDescription = re.compile(u"^\s+(?P<description>.*)", re.UNICODE)
        self.patModification = re.compile(u"^:(?P<perm1>\w+)\s+(?P<perm2>\w+)\s+(?P<hash1>[\w\.]+)\s+(?P<hash2>[\w\.]+)\s+(?P<type>\w+)\s+(?P<file>.*)$", re.UNICODE)

    def parse(self, repository):
        self.gotDescription = False
        self.commit = {}
        self.changes = {}
        self.allCommits = {}
        self.commitID = 0
 
        self.process = subprocess.Popen(['/usr/bin/git', 'log', '--raw'], shell=False, cwd=repository, stdout=subprocess.PIPE)
        self.output = self.process.communicate()[0]
        self.outputlines = re.split("\n", self.output)

        self.line = self.outputlines[0]
        self.uniline = unicode(self.line, errors='replace')
        self.m = self.patHash.match(self.uniline)
        self.commit['hash'] = self.m.group('hash')

        for self.line in self.outputlines[1:]:
            self.uniline = unicode(self.line, errors='replace')
            self.m = self.patHash.match(self.uniline)
            if self.m:
                self.commit['changes'] = self.changes
                self.allCommits[self.commitID] = self.commit
                self.commit = {}
                self.changes = {}
                self.gotDescription = False
                self.commentLine = ""
                self.commitID += 1

                self.commit['hash'] = self.m.group('hash')
            else:
                self.m = self.patAuthor.match(self.uniline)
                if self.m:
                    self.commit['author'] = self.m.group('author')
                else:
                    self.m = self.patDate.match(self.uniline)
                    if self.m:
                        self.commit['date'] = self.m.group('date')
                    else:
                        self.m = self.patEmpty.match(self.uniline)
                        if self.m:
                            continue 
                        else:
                            self.m = self.patDescription.match(self.uniline)
                            if self.m:
                                if not self.gotDescription:
                                    self.commit['description'] = self.m.group('description')
                                    self.gotDescription = True
                            else:
                                self.m = self.patModification.match(self.uniline)
                                if self.m:
                                    self.changes[self.m.group('file')] = { 
                                        'perm1': self.m.group('perm1'),
                                        'perm2': self.m.group('perm2'),
                                        'hash1': self.m.group('hash1'),
                                        'hash2': self.m.group('hash2'),
                                        'type' : self.m.group('type') }
                                else:
                                    self.m = self.patMerge.match(self.uniline)
                                    if self.m:
                                        pass
                                    else:
                                        print "FOUND UNKNOWN LINE:", self.uniline
                                        sys.exit(-10)

        self.commit['changes'] = self.changes
        self.allCommits[self.commitID] = self.commit

        return self.allCommits

    def getGitCommits(self):
      return self.allCommits

if __name__ == '__main__':
      a = GNOMEGitCommits()
      print a.parse('/tmp/GIT/zenity')

