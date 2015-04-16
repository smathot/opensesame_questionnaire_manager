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

import os
from PyQt4 import QtGui, uic


import questionnairecreator
from io_tools import get_resource_loc


class QuestionnaireCreatorUI(QtGui.QDialog):
    def __init__(self,lang,sourceFolder,kind):
        self.lang = lang
        self.sourceFolder = sourceFolder
        self.kind = kind
        self.fs = os.sep
        self.bgcolor = ['white','black']
        self.fgcolor = ['black','white']
        self.order = ['sequential','random']
        self.backend = ['legacy']
        self.resolutionHorizontal = 1024
        self.resolutionVertical = 768

        self.questions = ['vraag1','vraag2']
        self._id = ['1','2']

        super(QuestionnaireCreatorUI, self).__init__()
        self._initUI()

#        self.connect(self, Qt.SIGNAL('triggered()'), self.closeEvent )
#        QtGui.QWidget.__init__(self)

    def _initUI(self):

        if self.kind == 'mc':

            answers = 'No;Maybe;Yes'
            category = ['BIS;BAS','BIS']
            score =  ['0;1;2', '2;1;0' ]

        instruction = 'Please enter your answer'
        self.question_ui_path = get_resource_loc("questionnairecreator.ui")

#        question_ui_path = get_resource_loc("questionnairedialog_mc.ui")
        uic.loadUi(self.question_ui_path, self)
        self.addQuestionButton.clicked.connect(self.makeQuestionnaire)
        self.cancelButton.clicked.connect(self.reject)
        self.languageComboBox.addItems(self.lang)
        self.backendComboBox.addItems(self.backend)
        self.bgColorComboBox.addItems(self.bgcolor)
        self.fgColorComboBox.addItems(self.fgcolor)
        self.orderComboBox.addItems(self.order)
        self.questionPlainTextEdit.setPlainText('\n'.join(self.questions))
        self.idPlainTextEdit.setPlainText('\n'.join(self._id))
        self.resolutionHorizontalSpinBox.setValue(self.resolutionHorizontal)
        self.resolutionVerticalSpinBox.setValue(self.resolutionVertical)
        self.instructionPlainTextEdit.setPlainText(instruction)

        if self.kind == 'mc':
            self.infile = get_resource_loc('opensesame.script.mc')
            self.label.setText('Create MC Questionnaire')
            self.answerLineEdit.setText(answers)
            self.categoryPlainTextEdit.setPlainText('\n'.join(category))
            self.scorePlainTextEdit.setPlainText('\n'.join(score))
        elif self.kind == 'open':
            self.infile = get_resource_loc('opensesame.script.open')
            self.label.setText('Create Open Questionnaire')
            self.answerLineEdit.hide()
            self.categoryPlainTextEdit.hide()
            self.scorePlainTextEdit.hide()
            self.answerLabel.hide()
            self.categoryLabel.hide()
            self.scoreLabel.hide()

    def getValues(self):
        return [self.baseName, self.language]

    def makeQuestionnaire(self):
        name = unicode(self.nameLineEdit.text())
        bgcolor = unicode(self.bgColorComboBox.currentText())
        fgcolor = unicode(self.fgColorComboBox.currentText())
        backend = unicode(self.backendComboBox.currentText())
        order = unicode(self.orderComboBox.currentText())
        instruction = unicode(self.instructionPlainTextEdit.toPlainText())
        questions = unicode(self.questionPlainTextEdit.toPlainText())
        _id = unicode(self.idPlainTextEdit.toPlainText())
        self.language = unicode(self.languageComboBox.currentText())
        resolutionHorizontal = unicode(self.resolutionHorizontalSpinBox.value())
        resolutionVertical = unicode(self.resolutionVerticalSpinBox.value())

        if self.kind == 'mc':
            answers = unicode(self.answerLineEdit.text())
            category = unicode(self.categoryPlainTextEdit.toPlainText())
            score = unicode(self.scorePlainTextEdit.toPlainText())
        elif self.kind == 'open':
            answerString = None
            categoryList = None
            scoreList = None

#        if re.search('[a-zA-Z]', name) == None:
#            message = "Title should contain letters"
#            print(message)
#            #self.error = ErrorMessage(message)
#            return


        ## hier de variabelen nog weer omzetten
        questionList = questions.split('\n')
        idList = _id.split('\n')

        ## remove preceding and trailing spaces
        questionList = map(lambda it: it.strip(), questionList)
        idList = map(lambda it: it.strip(), idList)

        nquestions = len(questionList)
        n_id = len(idList)


        ## name check
        if (name == "") or (name == None):
            nameCheck = False
        else:
            nameCheck = True

        if self.kind == 'mc':
            categoryList = category.split('\n')
            scoreList = score.split('\n')
            answerList = answers.split(';')

            ## remove preceding and trailing spaces
            categoryList = map(lambda it: it.strip(), categoryList)
            scoreList = map(lambda it: it.strip(), scoreList)
            answerList = map(lambda it: it.strip(), answerList)

            answerString = ';'.join(answerList)

            ncategory = len(categoryList)
            nscore = len(scoreList)
            nanswers = len(answerList)

            ## check if all elements in score input field are numbers and if number of elements match number of elements in answerList


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


        self.baseName = name + '.opensesame.tar.gz'
        folderName = self.sourceFolder + self.fs + self.language
        fileName = folderName + self.fs + self.baseName


        if  os.path.isfile(fileName):
            fileNameCheck = False
        else:
            fileNameCheck = True


        if (self.kind == 'mc' and nquestions == n_id == ncategory == nscore and scoreCheck and nameCheck and numberCheck and fileNameCheck) or (self.kind == 'open' and nquestions == n_id and nameCheck and fileNameCheck):
            questionnairecreator.QuestionnaireCreator(self.infile, fileName, name, resolutionHorizontal, resolutionVertical, bgcolor, fgcolor, backend, instruction, order, questionList, idList, answerString, categoryList, scoreList, self.kind)
            self.done(0)
        elif not (self.kind == 'mc' and nquestions == n_id == ncategory == nscore and scoreCheck) or (self.kind == 'open' and nquestions == n_id):
            self.showErrorMessage('Not all fields have the correct number of elements')
        elif not nameCheck:
            self.showErrorMessage('No survey name specified')
        elif not numberCheck:
            self.showErrorMessage('Field \"score\" should contain only numbers, found other characters')
        elif not fileNameCheck:
            self.showErrorMessage('Filename already exist, please use another name.')


    def showErrorMessage(self,message):
        """
        Shows about window
        """

        error ="Error"

        msgBox = QtGui.QMessageBox(self)
        #msgBox.setWindowIcon(self.about_icon)
        msgBox.about(msgBox,error,message)