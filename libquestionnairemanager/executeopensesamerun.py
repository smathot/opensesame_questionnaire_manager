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
import subprocess

def runExperiment(pythonCommand, command, expFolder, logDestinationFileList, subjectNr, language, experimentList):




    fs = os.sep

    for index in range(len(experimentList)):

        fileName     = expFolder + fs + language + fs + experimentList[index]
        subjectArg   = u'--subject=' + subjectNr
        logArg       = u'--logfile=' + logDestinationFileList[index]
        screenArg    = u'--fullscreen'
        if pythonCommand != "":
            args = [pythonCommand, command, fileName, subjectArg, logArg, screenArg]
        else:
            args = [command, fileName, subjectArg, logArg, screenArg]
        #print(args)
        subprocess.call(args)

    sys.stdout.write('\nTotal process done!\n')
