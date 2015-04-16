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

#===================================================================
# Module with functions to save & restore qt widget values
# Written by: Alan Lilly
# Website: http://panofish.net
#===================================================================

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import inspect

#===================================================================
# save "ui" controls and values to registry "setting"
# currently only handles comboboxes editlines & checkboxes
# ui = qmainwindow object
# settings = qsettings object
#===================================================================

def guiSave(ui, settings,widString):

    #for child in ui.children():  # works like getmembers, but because it traverses the hierarachy, you would have to call guisave recursively to traverse down the tree


    for name, obj in inspect.getmembers(ui):
        #if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
        if isinstance(obj, QComboBox):
            name   = obj.objectName()      # get combobox name
            index  = obj.currentIndex()    # get current index from combobox
            text   = obj.itemText(index)   # get the text for current index
            settings.setValue(name, text)   # save combobox selection to registry

        if isinstance(obj, QLineEdit):
            name = obj.objectName()
            value = obj.text()
            settings.setValue(name, value)    # save ui values, so they can be restored next time

        if isinstance(obj, QCheckBox):
            name = obj.objectName()
            state = obj.isChecked()
            settings.setValue(name, state)


    name   = 'Listwidget'      # get combobox name
    #text   = obj.itemText(index)   # get the text for current index
    settings.setValue(name, widString)   # save combobox selection to registry


#===================================================================
# restore "ui" controls with values stored in registry "settings"
# currently only handles comboboxes, editlines &checkboxes
# ui = QMainWindow object
# settings = QSettings object
#===================================================================

def guiRestore(ui, settings):

    for name, obj in inspect.getmembers(ui):
        if isinstance(obj, QComboBox):
            index  = obj.currentIndex()    # get current region from combobox
            #text   = obj.itemText(index)   # get the text for new selected index
            name   = obj.objectName()

            value = settings.value(name)

            if value == "":
                continue

            index = obj.findText(value)   # get the corresponding index for specified string in combobox

            obj.setCurrentIndex(index)   # preselect a combobox value by index

        if isinstance(obj, QLineEdit):
            name = obj.objectName()
            value = settings.value(name)  # get stored value from registry
            obj.setText(value)  # restore lineEditFile

        if isinstance(obj, QCheckBox):
            name = obj.objectName()
            value = settings.value(name)   # get stored value from registry
            if value != None:
                obj.setChecked(stringToBool(value))   # restore checkbox

    name   = 'Listwidget'      # get combobox name
    #text   = obj.itemText(index)   # get the text for current index
    value = settings.value(name)

    return value


def stringToBool(string):
    if string == 'true' or string == 'True' or string == '1':
        return True
    elif string == 'false' or string == 'False' or string =='0':
        return False
    else:
        raise ValueError