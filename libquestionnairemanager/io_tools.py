# -*- coding: utf-8 -*-
"""
This file is part of OpenSesame Survey Manager

OpenSesame Survey Manager is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame Survey Manager is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Refer to <http://www.gnu.org/licenses/> for a copy of the GNU General Public License.

@author Bob Rosbag
"""

import sys
import os
from PyQt4 import QtCore, QtGui


class OutLog(object):
    """
    Class that intercepts stdout and stderr prints, and shows them in te QT
    textarea of the app.
    """
    def __init__(self, statusBox, out=None, color=None):
        """(statusBox, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.statusBox = statusBox
        self.out = out
        self.color = color

    def write(self, m):
        self.statusBox.moveCursor(QtGui.QTextCursor.End)
        if self.color:
            self.statusBox.setTextColor(self.color)

        self.statusBox.insertPlainText( m )
        # Make sure the messages are immediately shown
        QtCore.QCoreApplication.instance().processEvents()

        if self.out:
            self.out.write(m)


def get_resource_loc(item):
    """
    Determines the correct path to the required resource.
    When the app is packaged with py2exe or py2app, the locations of some images
    or resources may change. This function should correct for that


    Arguments:
        item (string)  - the item to locate

    Returns:
        (string) - the full path to the provided item

    """

    # When the app is packaged with py2app/exe or pyinstaller
    if getattr(sys, 'frozen', None):
        try:
            # If packaged with pyinstaller
            basedir = sys._MEIPASS
            return os.path.join(basedir,item)
        except:
            # If packaged with py2exe (but should also work for py2installer (not tested!) )
            basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
            if sys.platform == "win32":
                return os.path.join(basedir, "resources", item)
            elif sys.platform == "darwin":
                return os.path.join(basedir, "..", "Resources", "resources", item)

    # For Linux when installed through a repo
    elif os.name == 'posix' and os.path.exists('/usr/share/scoreprocessor/resources/'):
        return os.path.join('/usr/share/scoreprocessor/resources/', item)
    # When run from source
    else:
        basedir = os.path.dirname(__file__)
        return os.path.join(basedir,"..","resources",item)

def get_data_loc():
    """
    Determines the correct path to the required resource.
    When the app is packaged with py2exe or py2app, the locations of some images
    or resources may change. This function should correct for that


    Arguments:
        item (string)  - the item to locate

    Returns:
        (string) - the full path to the provided item

    """

    subjectmeasures = "subjectmeasures"

    # When the app is packaged with py2app/exe or pyinstaller
    if getattr(sys, 'frozen', None):
        try:
            # If packaged with pyinstaller
            basedir = sys._MEIPASS
            return basedir
        except:
            # If packaged with py2exe (but should also work for py2installer (not tested!) )
            basedir = os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
            normBaseDir = os.path.abspath(basedir)
            print(basedir)
            print(normBaseDir)
            if sys.platform == "win32":
                print(os.path.join(normBaseDir, subjectmeasures))
                return os.path.join(normBaseDir, subjectmeasures)
            elif sys.platform == "darwin":
                return os.path.join(normBaseDir, "..", subjectmeasures, subjectmeasures)

    # For Linux when installed through a repo
    elif os.name == 'posix' and os.path.exists('/usr/share/experimentmanager/subjectmeasures/'):
        return '/usr/share/experimentmanager/subjectmeasures/'
    # When run from source
    else:
        basedir = os.path.dirname(__file__)
        expdataPath = os.path.abspath(os.path.join(basedir,"..",subjectmeasures))

        return expdataPath

def getOpensesamerunCmd():

    if os.name == "nt":
        if os.path.isfile(u'C:\Program Files (x86)\OpenSesame\opensesamerun.exe'):
            command =  os.path.abspath(u'C:\Program Files (x86)\OpenSesame\opensesamerun.exe')
        elif os.path.isfile(u'C:\Program Files\OpenSesame\opensesamerun.exe'):
            command = os.path.abspath(u'C:\Program Files\OpenSesame\opensesamerun.exe')
        else:
            command = ""
    elif os.name == "posix":
        if os.path.isfile(u'/usr/bin/opensesamerun'):
            command       = u'opensesamerun'
        else:
            command = ""
    else:
        command = ""

    return command