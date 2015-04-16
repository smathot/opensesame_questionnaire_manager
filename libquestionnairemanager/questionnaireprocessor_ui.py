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
import calculatescore

from PyQt4 import QtCore, Qt, QtGui, uic
from PyQt4.QtWebKit import QWebView
from io_tools import OutLog, get_resource_loc


version = "1.0.0"
author = "Bob Rosbag"
email = "debian@bobrosbag.nl"

aboutString = """
Opensesame Survey Manager v{0}

Copyright 2015
{1}
{2}
""".format(version,author,email)

debug = False

class QuestionnaireProcessorUI(QtGui.QMainWindow):
    """
    QT User interface
    """
    def __init__(self):
        super(QuestionnaireProcessorUI, self).__init__()
        self._initUI()
        #self.connect(self, Qt.SIGNAL('triggered()'), self.closeEvent )
        #self.triggered.connect(self.closeEvent)


    def _initUI(self):
        """
        Initializes the UI and sets button actions
        """


        self.idKey                   = 'id'
        self.responseKey             = 'response'
        self.categoryKey             = 'category'
        self.answerOptionKey         = 'answer_options'
        self.answerScoreKey          = 'answer_options_scores'

        _id = ['1','2']
        category = ['BIS;BAS','BIS']
        answers = 'No;Maybe;Yes'
        score =  ['0;1;2', '2;1;0' ]

        # Load resources
        ui_path = get_resource_loc("questionnaireprocessor.ui")
        ico_path = get_resource_loc("questionnaireprocessor.png")
        helpimg_path = get_resource_loc("help-about.png")
        aboutimg_path = get_resource_loc("help-contents.png")
        labelimg_path = get_resource_loc("questionnaireprocessor.png")

        # icons
        self.help_icon = QtGui.QIcon(helpimg_path)
        self.about_icon = QtGui.QIcon(aboutimg_path)

        # Load and setup UI
        uic.loadUi(ui_path, self)
        self.setWindowIcon(QtGui.QIcon(ico_path))
        self.setFixedSize(606,889)
        self.center()
        self.setWindowTitle('OpenSesame Questionnaire Processor')
        self.docButton.setIcon(self.help_icon)
        self.aboutButton.setIcon(self.about_icon)
        self.idColumnLineEdit.setText(self.idKey)
        self.responseColumnLineEdit.setText(self.responseKey)
        self.categoryColumnLineEdit.setText(self.categoryKey)
        self.answerOptionColumnLineEdit.setText(self.answerOptionKey)
        self.answerScoreColumnLineEdit.setText(self.answerScoreKey)

        self.idCustomPlainTextEdit.setPlainText('\n'.join(_id))
        self.categoryCustomPlainTextEdit.setPlainText('\n'.join(category))
        self.answerCustomLineEdit.setText(answers)
        self.scoreCustomPlainTextEdit.setPlainText('\n'.join(score))
        self.statusBox.hide()
        self.statusBox.setReadOnly(True)

        pixmap = QtGui.QPixmap(labelimg_path)
        self.image.setPixmap(pixmap)

        if debug:
            self.statusBox.show()

        #self.rowCounter = -1
        #self.answerPlainTextEdit.setPlainText(u'No:0\nMaybe:1\nYes:2')
        #self.categoryPlainTextEdit.setPlainText(u'Extraversion:1,2,3\nNeuroticism:4,5,6')
#        self.show()

        ## hide custom elements
        self.idColumnLabel.hide()
        self.idColumnLineEdit.hide()
        self.responseColumnLabel.hide()
        self.responseColumnLineEdit.hide()
        self.categoryColumnLabel.hide()
        self.categoryColumnLineEdit.hide()
        self.answerOptionColumnLabel.hide()
        self.answerOptionColumnLineEdit.hide()
        self.answerScoreColumnLabel.hide()
        self.answerScoreColumnLineEdit.hide()
        self.line_2.hide()

        self.idCustomLabel.hide()
        self.idCustomPlainTextEdit.hide()
        self.categoryCustomLabel.hide()
        self.categoryCustomPlainTextEdit.hide()
        self.answerCustomLabel.hide()
        self.answerCustomLineEdit.hide()
        self.scoreCustomLabel.hide()
        self.scoreCustomPlainTextEdit.hide()
        self.customExperimentCheckBox.hide()



        # Set button actions
        self.inputFolderButton.clicked.connect(self.selectInputFolderLocation)
        self.outputFolderButton.clicked.connect(self.selectOutputFolderDestination)
#        self.addItemButton.clicked.connect(self.addItemToTable)
#        self.removeItemButton.clicked.connect(self.removeItemFromTable)
        self.processButton.clicked.connect(self.startAnalyze)
        self.docButton.clicked.connect(self.showDocWindow)
        self.aboutButton.clicked.connect(self.showAboutWindow)

        self.customColumnCheckBox.stateChanged.connect(self.updateCustomColumnWidgets)
        self.customExperimentCheckBox.stateChanged.connect(self.updateCustomExperimentWidgets)


        # Redirect console output to textbox in UI, printing stdout in black
        # and stderr in red
        sys.stdout = OutLog(self.statusBox, sys.stdout, QtGui.QColor(0,0,0))
        if not hasattr(sys,'frozen'):
            sys.stderr = OutLog(self.statusBox, sys.stderr, QtGui.QColor(255,0,0))
        else:
            sys.stderr = OutLog(self.statusBox, None, QtGui.QColor(255,0,0))
        print("")

        # The folders to read data files from
        self.sourceFolder = ""
        # the folder to write the output file to
        self.destinationFolder = ""

        self._lastSelectedDestDir = ""
        self._lastSelectedSourceDir = ""

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def updateCustomColumnWidgets(self):

        if self.customColumnCheckBox.isChecked() :
            self.idColumnLabel.show()
            self.idColumnLineEdit.show()
            self.responseColumnLabel.show()
            self.responseColumnLineEdit.show()
            self.categoryColumnLabel.show()
            self.categoryColumnLineEdit.show()
            self.answerOptionColumnLabel.show()
            self.answerOptionColumnLineEdit.show()
            self.answerScoreColumnLabel.show()
            self.answerScoreColumnLineEdit.show()
            self.line_2.show()

            self.customExperimentCheckBox.show()

            self.updateCustomExperimentWidgets()

        else:
            self.idColumnLabel.hide()
            self.idColumnLineEdit.hide()
            self.responseColumnLabel.hide()
            self.responseColumnLineEdit.hide()
            self.categoryColumnLabel.hide()
            self.categoryColumnLineEdit.hide()
            self.answerOptionColumnLabel.hide()
            self.answerOptionColumnLineEdit.hide()
            self.answerScoreColumnLabel.hide()
            self.answerScoreColumnLineEdit.hide()
            self.line_2.hide()

            self.customExperimentCheckBox.hide()
            self.idCustomLabel.hide()
            self.idCustomPlainTextEdit.hide()
            self.categoryCustomLabel.hide()
            self.categoryCustomPlainTextEdit.hide()
            self.answerCustomLabel.hide()
            self.answerCustomLineEdit.hide()
            self.scoreCustomLabel.hide()
            self.scoreCustomPlainTextEdit.hide()
            self.customExperimentCheckBox.hide()


    def updateCustomExperimentWidgets(self):

        if self.customExperimentCheckBox.isChecked():
            self.idCustomLabel.show()
            self.idCustomPlainTextEdit.show()
            self.categoryCustomLabel.show()
            self.categoryCustomPlainTextEdit.show()
            self.answerCustomLabel.show()
            self.answerCustomLineEdit.show()
            self.scoreCustomLabel.show()
            self.scoreCustomPlainTextEdit.show()

            self.categoryColumnLabel.hide()
            self.categoryColumnLineEdit.hide()
            self.answerOptionColumnLabel.hide()
            self.answerOptionColumnLineEdit.hide()
            self.answerScoreColumnLabel.hide()
            self.answerScoreColumnLineEdit.hide()



        else:
            self.idCustomLabel.hide()
            self.idCustomPlainTextEdit.hide()
            self.categoryCustomLabel.hide()
            self.categoryCustomPlainTextEdit.hide()
            self.answerCustomLabel.hide()
            self.answerCustomLineEdit.hide()
            self.scoreCustomLabel.hide()
            self.scoreCustomPlainTextEdit.hide()

            self.categoryColumnLabel.show()
            self.categoryColumnLineEdit.show()
            self.answerOptionColumnLabel.show()
            self.answerOptionColumnLineEdit.show()
            self.answerScoreColumnLabel.show()
            self.answerScoreColumnLineEdit.show()



    def center(self):
        """
        Centers the main app window on the screen
        """
        qr = self.frameGeometry()
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def selectInputFolderLocation(self):
        """
        Select folder to read csv files from
        """
        selectedFolder = unicode(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.inputFolderLocation.text()))
        # Prevent erasing previous entry on cancel press
        if selectedFolder:
            self.sourceFolder = selectedFolder
            self.inputFolderLocation.setText(os.path.normpath(self.sourceFolder))
            self.progressBar.setValue(0)

    def selectOutputFolderDestination(self):
        """
        Set file to write output to
        """
        selectedDest = unicode(QtGui.QFileDialog.getExistingDirectory(self,"Save output in..", directory=self.outputFolderDestination.text()))
        # Prevent erasing previous entry on cancel press
        if selectedDest:
            self.destinationFolder = selectedDest
            self.outputFolderDestination.setText(os.path.normpath(unicode(self.destinationFolder)))
            self.progressBar.setValue(0)

    def startAnalyze(self):
        """
        Starts the merge operation. Uses sheet_io_tools for this.
        """

        if self.sourceFolder == "":
            print >> sys.stderr, "Please select a source folder containing the data files to merge."
            self.showErrorMessage("Please select a source folder containing the data files to merge.")

        elif self.destinationFolder == "":
            print >> sys.stderr, "Please specify a folder to save the results."
            self.showErrorMessage("Please specify a folder to save the results.")


        else:
            print("Starting Analyze operation...")



            responseKey = self.responseKey
            idKey = self.idKey
            categoryKey = self.categoryKey
            answerOptionKey = self.answerOptionKey
            answerScoreKey = self.answerScoreKey


            idList = None
            categoryList = None
            answerList = None
            scoreList = None



            if self.customColumnCheckBox.isChecked() == False:

                custom = False
                analyzedDataset = calculatescore.analyzeQuestionnaire(self.sourceFolder, self.destinationFolder, responseKey, idKey, categoryKey, answerOptionKey, answerScoreKey, idList, categoryList, answerList, scoreList, custom, self.progressBar)

                if analyzedDataset:
                    print("Output saved to " + self.destinationFolder)
                    print("Ready.")

            elif self.customColumnCheckBox.isChecked() and self.customExperimentCheckBox.isChecked() == False:
                responseKey = unicode(self.responseColumnLineEdit.text())
                idKey = unicode(self.idColumnLineEdit.text())
                categoryKey = unicode(self.categoryColumnLineEdit.text())
                answerOptionKey = unicode(self.answerOptionColumnLineEdit.text())
                answerScoreKey = unicode(self.answerScoreColumnLineEdit.text())
                custom = False
                if responseKey != "" and idKey != "" and categoryKey != "" and answerOptionKey != "" and answerScoreKey != "":

                    analyzedDataset = calculatescore.analyzeQuestionnaire(self.sourceFolder, self.destinationFolder, responseKey, idKey, categoryKey, answerOptionKey, answerScoreKey, idList, categoryList, answerList, scoreList, custom, self.progressBar)

                    if analyzedDataset:
                        print("Output saved to " + self.destinationFolder)
                        print("Ready.")
                else:
                    print >> sys.stderr, "Not all column names are defined."
                    self.showErrorMessage("Not all column names are defined.")


            elif self.customColumnCheckBox.isChecked() and self.customExperimentCheckBox.isChecked():


                rawId = unicode(self.idCustomPlainTextEdit.toPlainText())
                rawAnswers = unicode(self.answerCustomLineEdit.text())
                rawCategory = unicode(self.categoryCustomPlainTextEdit.toPlainText())
                rawScore = unicode(self.scoreCustomPlainTextEdit.toPlainText())

                idList = rawId.split('\n')
                categoryList = rawCategory.split('\n')
                scoreList = rawScore.split('\n')

                idList = map(lambda it: it.strip(), idList)
                categoryList = map(lambda it: it.strip(), categoryList)
                scoreList = map(lambda it: it.strip(), scoreList)

                rawAnswerListTemp = rawAnswers.split(';')
                rawAnswerListTemp = map(lambda it: it.strip(), rawAnswerListTemp)
                nanswers = len(rawAnswerListTemp)
                answers = ';'.join(rawAnswerListTemp)

                answerList = []
                for index in range(len(idList)):
                    answerList.append(answers)

                custom = True


                ## checks

                ncategory = len(categoryList)
                nscore = len(scoreList)
                n_id = len(idList)

                nScoreItemList = []
                checkList = []
                for item in scoreList:
                    scoreItemList = item.split(';')
                    nScoreItemList.append(len(scoreItemList))
                    checkList.append(all(element.isdigit()==True for element in scoreItemList))

                numberCheck = all(item==True for item in checkList)

                uniqueScoreItemList = list(set(nScoreItemList))
                if len(uniqueScoreItemList)==1:

                    uniqueItems = uniqueScoreItemList[0]
                    if uniqueItems == nanswers:
                        scoreCheck = True
                    else:
                        scoreCheck = False
                else:
                    scoreCheck = False

                ## cum checks
                if n_id == ncategory == nscore and scoreCheck and numberCheck:
                    analyzedDataset = calculatescore.analyzeQuestionnaire(self.sourceFolder, self.destinationFolder, responseKey, idKey, categoryKey, answerOptionKey, answerScoreKey, idList, categoryList, answerList, scoreList, custom, self.progressBar)

                    if analyzedDataset:
                        print("Output saved to " + self.destinationFolder)
                        print("Ready.")
                elif not (n_id == ncategory == nscore and scoreCheck):
                    self.showErrorMessage('Not all fields have the correct number of elements')
                elif not numberCheck:
                    self.showErrorMessage('Field \"score\" should contain only numbers, found other characters')

    def showErrorMessage(self,message):
        """
        Shows about window
        """

        error ="Error"

        msgBox = QtGui.QMessageBox(self)
        #msgBox.setWindowIcon(self.about_icon)
        msgBox.about(msgBox,error,message)

    def showDocWindow(self):
        """
        Shows documentation window (with help and licensing info)
        """
        self.docWindow = QWebView()
        self.docWindow.closeEvent = self.closeDocWindow
        self.docWindow.setWindowTitle("Documentation")
        self.docWindow.setWindowIcon(self.help_icon)
        self.docWindow.load(QtCore.QUrl(get_resource_loc("helpfile.html")))
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
        global aboutstring
        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowIcon(self.about_icon)
        msgBox.about(msgBox,"About",aboutString)

