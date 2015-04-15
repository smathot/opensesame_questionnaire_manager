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

from __future__ import division
from __future__ import unicode_literals

import sys
import os
import executeopensesamerun
import profile
import questionnairecreator_ui

from PyQt4 import QtCore, Qt, QtGui, uic
from PyQt4.QtWebKit import QWebView
from tools import OutLog, get_resource_loc, get_data_loc, getOpensesamerunCmd

version = "1.0.0"
author = "Bob Rosbag"
email = "debian@bobrosbag.nl"

aboutString = """
ScoreProcessor v{0}

Copyright 2015
{1}
{2}
""".format(version,author,email)


class QuestionnaireManagerUI(QtGui.QMainWindow):
    """
    QT User interface
    """
    def __init__(self):
        super(QuestionnaireManagerUI, self).__init__()
        self.fs = os.sep
        self._initUI()


        self.lang = []
        self.comboBoxItemList = []
        self.experimentDict = {}
        self.widgetDict = {}
        self.widgetNameDict = {}

        self.processDirs()
        self.createComboBoxItems()
        self.createListWidget()
        self.updateListWidget()
        self.comboBox.currentIndexChanged.connect(self.updateListWidget)
#        self.comboBox.currentIndexChanged.connect(self.refreshWidgets)
        self.connect(self, Qt.SIGNAL('triggered()'), self.closeEvent )


    def _initUI(self):
        """
        Initializes the UI and sets button actions
        """
#        QtGui.QMainWindow.__init__(self)


        # Load resources
        ui_path = get_resource_loc("questionnairemanager.ui")
        ico_path = get_resource_loc("questionnairemanager.png")
        helpimg_path = get_resource_loc("help-about.png")
        aboutimg_path = get_resource_loc("help-contents.png")
        labelimg_path = get_resource_loc("questionnairemanager.png")

        # icons
        self.help_icon = QtGui.QIcon(helpimg_path)
        self.about_icon = QtGui.QIcon(aboutimg_path)

        self.command = getOpensesamerunCmd()
        self.defaultOpensesame = 'C:\Program Files\OpenSesame'

        # Load and setup UI
        uic.loadUi(ui_path, self)
        self.setWindowIcon(QtGui.QIcon(ico_path))
        self.setFixedSize(538,819)
        self.center()
        self.setWindowTitle('OpenSesame Questionnaire Manager')
        self.docButton.setIcon(self.help_icon)
        self.aboutButton.setIcon(self.about_icon)
        self.srcCheckBox.setChecked(False)
        self.pythonLabel.hide()
        self.pythonLineEdit.hide()
        self.pythonButton.hide()
        self.statusBox.setReadOnly(True)
        self.statusBox.hide()
        pixmap = QtGui.QPixmap(labelimg_path)
        self.image.setPixmap(pixmap)


        # set parameters for listWidget
        #self.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
#        self.listWidget.DropIndicatorPosition(QtGui.QAbstractItemView.AboveItem)
        if self.command == "":
            self.opensesamerunLabel.show()
            self.opensesamerunLineEdit.show()
            self.opensesamerunButton.show()
            self.opensesameNotFoundLabel.show()

        else:
            self.opensesamerunLabel.hide()
            self.opensesamerunLineEdit.hide()
            self.opensesamerunButton.hide()
            self.opensesameNotFoundLabel.hide()

        #self.show()

        # Set button actions
        self.inputFolderButton.clicked.connect(self.selectInputFolderLocation)
        self.logFolderButton.clicked.connect(self.selectLogFolderDestination)
        self.startButton.clicked.connect(self.startExperiment)
        self.docButton.clicked.connect(self.showDocWindow)
        self.aboutButton.clicked.connect(self.showAboutWindow)
        self.restoreGuiButton.clicked.connect(self.selectOpenGuiFile)
        self.saveGuiButton.clicked.connect(self.selectSaveGuiFile)
        self.opensesamerunButton.clicked.connect(self.selectOpensesamerunFile)
        self.pythonButton.clicked.connect(self.selectPythonFile)
        self.createOpenButton.clicked.connect(self.addOpenQuestion)
        self.createMCButton.clicked.connect(self.addMCQuestion)
        self.refreshButton.clicked.connect(self.refreshWidgets)

        self.srcCheckBox.stateChanged.connect(self.updaterunFromSource)

        # Redirect console output to textbox in UI, printing stdout in black
        # and stderr in red
        sys.stdout = OutLog(self.statusBox, sys.stdout, QtGui.QColor(0,0,0))
        if not hasattr(sys,'frozen'):
            sys.stderr = OutLog(self.statusBox, sys.stderr, QtGui.QColor(255,0,0))
        else:
            sys.stderr = OutLog(self.statusBox, None, QtGui.QColor(255,0,0))
        print("")

        # The folders to read data files from
        self.sourceFolder = get_data_loc()
        self.inputFolderLocation.setText(self.sourceFolder)
        print(self.sourceFolder)

        # the folder to write the output file to
        self.destinationFolder = ""
        self.locationopensesamerun = ""
        self.locationPython = ""
        self._lastSelectedDestDir = ""
        self._lastSelectedSourceDir = ""
        self.pythonCommand = ""


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

    def center(self):
        """
        Centers the main app window on the screen
        """
        qr = self.frameGeometry()
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addMCQuestion(self):

        self.mc = questionnairecreator_ui.QuestionnaireCreatorUI(self.lang,self.sourceFolder,'mc')
        self.mc.exec_()
        self.refreshWidgets()

    def addOpenQuestion(self):

        self.open = questionnairecreator_ui.QuestionnaireCreatorUI(self.lang,self.sourceFolder,'open')
        self.open.exec_()        
        self.refreshWidgets()

    def saveGui(self):

        [selectedExperimentList, selectedLanguage] = self.getSelectedExperimentData()
        profile.guiSave(self.ui,self.settingsSave,selectedExperimentList)

    def restoreGui(self):

        selectedExperimentList = profile.guiRestore(self.ui,self.settingsRestore)

        nWidgets = self.listWidget.count()
        for index in range(nWidgets):
            self.listWidget.item(index).setCheckState(QtCore.Qt.Unchecked)

        for index in range(len(selectedExperimentList)):

            [listWidgetItem] = self.listWidget.findItems(selectedExperimentList[index],QtCore.Qt.MatchExactly)
            currentIndex = self.listWidget.row(listWidgetItem)
            targetWidget = self.listWidget.takeItem(currentIndex)
            targetWidget.setCheckState(QtCore.Qt.Checked)
            self.listWidget.insertItem(index,targetWidget)


    def selectSaveGuiFile(self):
        """
        Set file to write output to
        """
        selectedGuiDest = unicode(QtGui.QFileDialog.getSaveFileName(self,"Save output as..",'default.ini',"INI (*.ini)"))
        # Prevent erasing previous entry on cancel press
        if selectedGuiDest:
            self.destinationGuiFile = selectedGuiDest
            self.settingsSave = QtCore.QSettings(self.destinationGuiFile, QtCore.QSettings.IniFormat)
            self.saveGui()

    def selectOpenGuiFile(self):
        """
        Set file to write output to
        """
        selectedGuiLocation = unicode(QtGui.QFileDialog.getOpenFileName(self,"Open File..",'default.ini',"INI (*.ini)"))
        # Prevent erasing previous entry on cancel press
        if selectedGuiLocation:
            self.locationGuiFile = selectedGuiLocation
            self.settingsRestore = QtCore.QSettings(self.locationGuiFile, QtCore.QSettings.IniFormat)
            self.restoreGui()

    def selectOpensesamerunFile(self):
        """
        Set file to write output to
        """
        selectedopensesamerunLocation = unicode(QtGui.QFileDialog.getOpenFileName(self,"Open File.."))
        # Prevent erasing previous entry on cancel press
        if selectedopensesamerunLocation:
            self.locationopensesamerun = selectedopensesamerunLocation
            self.opensesamerunLineEdit.setText(os.path.normpath(self.locationopensesamerun))
#            self.manualCommand = os.path.normpath(self.locationopensesamerun)

    def selectPythonFile(self):
        """
        Set file to write output to
        """
        selectedpythonLocation = unicode(QtGui.QFileDialog.getOpenFileName(self,"Open File.."))
        # Prevent erasing previous entry on cancel press
        if selectedpythonLocation:
            self.locationPython = selectedpythonLocation
            self.pythonLineEdit.setText(os.path.normpath(self.locationPython))
#            self.pythonCommand = os.path.normpath(self.locationPython)

    def selectInputFolderLocation(self):
        """
        Select folder to read csv files from
        """
        selectedFolder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.inputFolderLocation.text()))
        # Prevent erasing previous entry on cancel press
        if selectedFolder:
            self.sourceFolder = selectedFolder
            self.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
            self.refreshWidgets()

    def selectLogFolderDestination(self):
        """
        Set file to write output to
        """
        selectedDest = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.logFolderDestination.text()))
        # Prevent erasing previous entry on cancel press
        if selectedDest:
            self.destinationFolder = selectedDest
            self.logFolderDestination.setText(os.path.normpath(unicode(self.destinationFolder)))

    def refreshWidgets(self):
        self.updateDirs()
        self.updateListWidgetItems()
        self.updateComboBoxItems()
        self.emptyListWidget()
        self.fillListWidget()

    def processDirs(self):

        for _dir in os.listdir(self.sourceFolder):
            languageDir = self.sourceFolder + self.fs + _dir
            if os.path.isfile(languageDir):
                pass
            else:
                self.lang.append(_dir)
                self.experimentDict[_dir] = []

                for expFile in sorted(os.listdir(languageDir)):
                    filePath = languageDir + self.fs + expFile
                    if os.path.isfile(filePath):
                        self.experimentDict[_dir].append(expFile)

        self.lang = sorted(self.lang)

    def updateDirs(self):
        langList = list(self.lang)

        for _dir in os.listdir(self.sourceFolder):
            languageDir = self.sourceFolder + self.fs + _dir
            if os.path.isfile(languageDir):
                pass
            else:
                if _dir not in langList:
                    self.lang.append(_dir)
                    self.experimentDict[_dir] = []
                for expFile in sorted(os.listdir(languageDir)):
                    filePath = languageDir + self.fs + expFile
                    if os.path.isfile(filePath):
                        if expFile not in self.experimentDict[_dir]:
                            self.experimentDict[_dir].append(expFile)

        for lang in langList:
            languageDir = self.sourceFolder + self.fs + lang

            if os.path.isdir(languageDir) == False:
                self.lang.remove(lang)
                self.experimentDict.pop(lang, None)
            else:
                for expFile in self.experimentDict[lang]:
                    filePath = languageDir + self.fs + expFile
                    if os.path.isfile(filePath) == False:
                        self.experimentDict[lang].remove(expFile)

    def createComboBoxItems(self):

        for lang in self.lang:
            self.comboBox.addItem(lang)
            self.comboBoxItemList.append(lang)

    def updateComboBoxItems(self):

        comboBoxItemList = list(self.comboBoxItemList)

        for lang in self.lang:
            if lang not in comboBoxItemList:
                self.comboBox.addItem(lang)
                self.comboBoxItemList.append(lang)

        for lang in comboBoxItemList:
            if lang not in self.lang:

                if self.comboBox.currentText() == lang:
                    index1 = self.comboBox.findText(self.lang[0],QtCore.Qt.MatchExactly)
                    self.comboBox.setCurrentIndex(index1)

                self.comboBoxItemList.remove(lang)
                index = self.comboBox.findText(lang,QtCore.Qt.MatchExactly)
                self.comboBox.removeItem(index)

    def createListWidget(self):

        for lang in self.lang:
            expnameList = self.experimentDict[lang]
            listWidgetItemList = []
            widgetItemList = []
            for index in range(len(expnameList)):
                widgetItem = unicode(expnameList[index])
                widgetItemList.append(widgetItem)
                listWidgetItem = self.createListWidgetItem(widgetItem)
                listWidgetItemList.append(listWidgetItem)

            self.widgetDict[lang] = listWidgetItemList
            self.widgetNameDict[lang] = widgetItemList


    def emptyListWidget(self):

        while self.listWidget.count() > 0:

            self.listWidget.takeItem(0)

    def fillListWidget(self):

        lang = unicode(self.comboBox.currentText())
        listWidgetItemList = self.widgetDict[lang]

        for row in range(len(listWidgetItemList)):
            self.listWidget.insertItem(row,listWidgetItemList[row])
            self.listWidget.item(row).setCheckState(QtCore.Qt.Checked)


    def updateListWidget(self):
        self.emptyListWidget()
        self.fillListWidget()


    def createListWidgetItem(self, widgetItem):

        listWidgetItem = QtGui.QListWidgetItem(widgetItem)
        listWidgetItem.setCheckState(QtCore.Qt.Checked)
        listWidgetItem.setFlags( QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled )

        return listWidgetItem


    def updateListWidgetItems(self):

        widgetNameDictKeys =  list(self.widgetNameDict.keys())

        for lang in self.lang:
            expnameList = self.experimentDict[lang]
            if lang not in widgetNameDictKeys:
                self.widgetNameDict[lang] = []
                self.widgetDict[lang] = []

            for index in range(len(expnameList)):

                widgetItem = expnameList[index]

                if widgetItem not in self.widgetNameDict[lang]:
                    listWidgetItem = self.createListWidgetItem(widgetItem)

                    self.widgetDict[lang].append(listWidgetItem)
                    self.widgetNameDict[lang].append(widgetItem)


        for lang in widgetNameDictKeys:

            if lang not in self.lang:
                self.emptyListWidget()

                self.widgetDict.pop(lang, None)
                self.widgetNameDict.pop(lang, None)
            else:
                for widgetItem in self.widgetNameDict[lang]:
                    if widgetItem not in self.experimentDict[lang]:
                        self.emptyListWidget()

                        self.widgetNameDict[lang].remove(widgetItem)
                        [listWidgetItem] = self.listWidget.findItems(widgetItem,QtCore.Qt.MatchExactly)
                        self.widgetDict[lang].remove(listWidgetItem)

    def getSelectedExperimentData(self):

        selectedExperimentList = []
        selectedLanguage = unicode(self.comboBox.currentText())

        nWidgets = self.listWidget.count()
        for index in range(nWidgets):
            listWidgetItem = self.listWidget.item(index)
            if listWidgetItem.checkState() == 2:
                selectedExperimentList.append(listWidgetItem.text())
        #print(selectedExperimentList)

        return [selectedExperimentList, selectedLanguage]

    def updaterunFromSource(self):
        if self.srcCheckBox.isChecked():
            self.pythonLabel.show()
            self.pythonLineEdit.show()
            self.pythonButton.show()
            self.opensesamerunLabel.show()
            self.opensesamerunLineEdit.show()
            self.opensesamerunButton.show()
        elif self.srcCheckBox.isChecked() == False:
            self.pythonLabel.hide()
            self.pythonLineEdit.hide()
            self.pythonButton.hide()
            if self.command == "":
                self.opensesamerunLabel.show()
                self.opensesamerunLineEdit.show()
                self.opensesamerunButton.show()
            else:
                self.opensesamerunLabel.hide()
                self.opensesamerunLineEdit.hide()
                self.opensesamerunButton.hide()

    def startExperiment(self):
        """
        Starts the merge operation. Uses sheet_io_tools for this.
        """

        self.pythonCommand = unicode(self.pythonLineEdit.text())
        self.manualCommand = unicode(self.opensesamerunLineEdit.text())
        self.destinationFolder = unicode(self.logFolderDestination.text())

        if self.sourceFolder == "":
            print >> sys.stderr, "Please select a source folder containing the experiment files."
            self.showErrorMessage("Please select a source folder containing the experiment files.")
#        elif self.destinationFolder == "":
#            print >> sys.stderr, "Please specify a folder for the log files."
        elif unicode(self.subjectLineEdit.text()).isdigit() == False:
            print >> sys.stderr, "Please enter an integer as subject number."
            self.showErrorMessage("Please enter an integer as subject number.")

        elif self.command == "" and self.locationopensesamerun == "":
            print >> sys.stderr, "Please specify the path to opensesamerun."
            self.showErrorMessage("Please specify the path to opensesamerun.")
        elif self.srcCheckBox.isChecked() and self.manualCommand == "":
            print >> sys.stderr, "Please specify the path to opensesamerun."
            self.showErrorMessage("Please specify the path to opensesamerun.")

        else:
            if self.srcCheckBox.isChecked():
                self.opensesamerunCommand = self.manualCommand

            elif self.srcCheckBox.isChecked() == False:
                if self.command == "":
                    self.opensesamerunCommand = self.manualCommand
                else:
                    self.opensesamerunCommand = self.command
                ## reset python cmd if checkbox is unchecked
                if self.locationPython != "":
                    self.pythonCommand = ""

            [selectedExperimentList, selectedLanguage] = self.getSelectedExperimentData()


            for experiment in selectedExperimentList:
                strippedExperiment = experiment.replace('.opensesame.tar.gz','')
                strippedExperiment = strippedExperiment.replace('.opensesame','')
                destinationFolder = self.destinationFolder + self.fs + selectedLanguage + self.fs + strippedExperiment + self.fs
                try:
                    os.makedirs(destinationFolder)
                except OSError as exc: # Python >2.5
                    if exc.errno == errno.EEXIST and os.path.isdir(path):
                        pass
                    else: raise



            selectedSubjectNr = unicode(self.subjectLineEdit.displayText())

            print("Starting Experiment...")
            finishedExperiment = executeopensesamerun.runExperiment(self.pythonCommand, self.opensesamerunCommand ,self.sourceFolder, destinationFolder, selectedSubjectNr, selectedLanguage, selectedExperimentList)
            if finishedExperiment:
                print("Output saved to " + self.destinationFolder)
                print("Ready.")


    def showDocWindow(self):
        """
        Shows documentation window (with help and licensing info)
        """

        title = "Documentation"
        htmlFile = "helpfile.html"

        self.docWindow = QWebView()
        self.docWindow.closeEvent = self.closeDocWindow
        self.docWindow.setWindowTitle(title)
        self.docWindow.setWindowIcon(self.help_icon)
        self.docWindow.load(QtCore.QUrl(get_resource_loc(htmlFile)))
        self.docWindow.show()

    def closeDocWindow(self,source):
        """
        Callback function of the docWindow QWebView item.
        Destroys reference to doc window after its closed
        """
        del(self.docWindow)

    def showAboutWindow(self):
        """
        Shows about window
        """

        about ="About"

        global aboutstring
        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowIcon(self.about_icon)
        msgBox.about(msgBox,about,aboutString)

    def showErrorMessage(self,message):
        """
        Shows about window
        """

        error ="Error"

        msgBox = QtGui.QMessageBox(self)
        #msgBox.setWindowIcon(self.about_icon)
        msgBox.about(msgBox,error,message)