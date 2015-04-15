# -*- coding: utf-8 -*-
"""
This file is part of ScoreProcessor

ScoreProcessor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Datamerger is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Refer to <http://www.gnu.org/licenses/> for a copy of the GNU General Public License.

@author Bob Rosbag
"""

from __future__ import division
from __future__ import unicode_literals

import os
import sys


def runExperiment(pythonCommand, command, expFolder, destinationFolder, subjectNr, language, experimentList):

    if not os.path.isdir(destinationFolder):
        print >> sys.stderr, "ERROR: the specified folder " + destinationFolder + " is invalid"
        return False

    import subprocess

    fs = os.sep

    for experiment in experimentList:

        fileName     = expFolder + fs + language + fs + experiment
        subjectArg   = u'--subject=' + unicode(subjectNr)
        logArg       = u'--logfile=' + destinationFolder + fs + u'subject-' + unicode(subjectNr) + u'.csv'
        screenArg    = u'--fullscreen'
        if pythonCommand != "":
            args = [pythonCommand, command, fileName, subjectArg, logArg, screenArg]
        else:
            args = [command, fileName, subjectArg, logArg, screenArg]
        #print(args)
        subprocess.call(args)

    sys.stdout.write('\nTotal process done!\n')
