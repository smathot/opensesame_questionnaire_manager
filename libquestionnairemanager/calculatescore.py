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

import glob
import numpy as np
import os
import csv
import sys
import re
import codecs, cStringIO
from PyQt4 import QtGui

fs = os.sep

def analyzeQuestionnaire(dataFolder, destinationFolder, responseKey, idKey, categoryKey, answerOptionKey, answerScoreKey, customId, customCategory, customAnswers, customScore, custom, progressBar):

    if not os.path.isdir(dataFolder):
        print >> sys.stderr, "ERROR: the specified folder " + dataFolder + " is invalid"
        showErrorMessage("ERROR: the specified folder " + dataFolder + " is invalid")

        return False

#    response       = 'response'
    dataExt                 = '.csv'
    resultExt               = '.txt'

    delimiter               = str('\t')
    scoreTypeList           = ['Sum', 'Mean']

    dataFolderList    = listDataFolders(dataFolder)

    if dataFolderList == []:
        dataFolderList = [dataFolder]
        singleFolder = True
    else:
        singleFolder = False

    if singleFolder == False and custom == True:
        print >> sys.stderr, "\nError: Processing a custom experiment works only with a single experiment, multiple experiments are not supported in this mode"
        showErrorMessage("Error: Processing a custom experiment works only with a single experiment, multiple experiments are not supported in this mode")

        return

    totalFiles = 0

    for dataFolder in dataFolderList:
        nrDataFile    = len(listDataFiles(dataFolder, dataExt))
        totalFiles += nrDataFile

    counter = 0

    for dataFolder in dataFolderList:

        ## find data files and put file names in list and array
        dataFileList    = listDataFiles(dataFolder, dataExt)


        ## start counter and progressbar

        if not progressBar is None:
            progressBar.setValue(0)


        subjectResponseDict = {}
        subjectCategoryDict = {}
        fileNameList = []
        for dataFile in dataFileList:

            fileName = os.path.basename(dataFile)
            sys.stdout.write(fileName)

            dataDict = readCsv(dataFile)
            fileNameList.append(fileName)
            ## make lists with the dependent variables from the dict



            try:
                responseList     = list(dataDict[responseKey])

            except:

                print >> sys.stderr, "\nError: Column with name: " + responseKey + " is not present in the data file, please try custom experiment"
                showErrorMessage("Error: Column with name: " + responseKey + " is not present in the data file, please try custom experiment")

                return


            if custom:
                idList = customId
                rawCategoryList = customCategory
                rawAnswerOptionList = customAnswers
                rawAnswerOptionScoreList = customScore
            else:

                try:
                    idList           = dataDict[idKey]
                except:
                    print >> sys.stderr, "\nError: Column with name: " + idKey + " is not present in the data file, please try custom experiment"
                    showErrorMessage("Error: Column with name: " + idKey + " is not present in the data file, please try custom experiment")
                    return


                try:
                    rawCategoryList     = dataDict[categoryKey]

                except:
                    print >> sys.stderr, "\nError: Column with name: " + categoryKey + " is not present in the data file, please try custom experiment"
                    showErrorMessage("Error: Column with name: " + categoryKey + " is not present in the data file, please try custom experiment")
                    return

                try:
                    rawAnswerOptionList       = dataDict[answerOptionKey]

                except:
                    print >> sys.stderr, "\nError: Column with name: " + answerOptionKey + " is not present in the data file, please try custom experiment"
                    showErrorMessage("Error: Column with name: " + answerOptionKey + " is not present in the data file, please try custom experiment")

                    return

                try:
                    rawAnswerOptionScoreList  = dataDict[answerScoreKey]

                except:
                    print >> sys.stderr, "\nError: Column with name: " + answerScoreKey + " is not present in the data file, please try custom experiment"
                    showErrorMessage("Error: Column with name: " + answerScoreKey + " is not present in the data file, please try custom experiment")

                    return



            ## make arrays with the dependent variables data
            idList = map(lambda it: it.strip(), idList)
            #idArray                = np.array(idList, dtype=np.uint8)

            responseDict = {}
            answerScoreDict = {}
            categoryDict = {}
            for index in range(len(idList)):

                ## make categoryDict
                CategoryList = rawCategoryList[index].split(';')
                CategoryList = map(lambda it: it.strip(), CategoryList)

                categoryDict[idList[index]] = CategoryList

                ## make answerScoreDict
                answerList = rawAnswerOptionList[index].split(';')
                answerList = map(lambda it: it.strip(), answerList)

#               case insensitive maken

                scoreList  = rawAnswerOptionScoreList[index].split(';')
                scoreList = map(lambda it: it.strip(), scoreList)

                answerDict = {}

                for subindex in range(len(answerList)):
                    answerDict[answerList[subindex]] = scoreList[subindex]
                answerScoreDict[idList[index]] = answerDict

                ## make reponseDict
                responseDict[idList[index]] = responseList[index]
#               case insensitive maken

            individualScoreDict = {}
            categoryScoreDict = {}
            sortedIdList = sorted(idList)
            for index in range(len(sortedIdList)):
                selectedId = sortedIdList[index]

                response = responseDict[selectedId]

                categories = categoryDict[selectedId]
                scoreDict = answerScoreDict[selectedId]

                try:
                    score = scoreDict[response]

                except:
                    print >> sys.stderr, "\nError: Response: " + response + " is unknown"
                    showErrorMessage("Error: Response: " + response + " is unknown")

                    return


                individualScoreDict[selectedId] = score

                for category in categories:
                    if category in categoryScoreDict:
                        categoryScoreDict[category].append(score)
                    else:
                        categoryScoreDict[category] = [score]

            subjectResponseDict[fileName] = individualScoreDict
            uniCategoryList = categoryScoreDict.keys()
            uniCategoryScoreDict = {}

            for uniCategory in uniCategoryList:
                uniCategoryScoreList = categoryScoreDict[uniCategory]
                uniCategoryScoreArray = np.array(uniCategoryScoreList, dtype='d')

                sumUniCategoryScoreString = unicode(np.sum(uniCategoryScoreArray))
                meanUniCategoryScoreString = unicode(np.mean(uniCategoryScoreArray))

                uniCategoryScoreDict1 = {}
                uniCategoryScoreDict1['Sum'] = sumUniCategoryScoreString
                uniCategoryScoreDict1['Mean'] = meanUniCategoryScoreString
                uniCategoryScoreDict[uniCategory] = uniCategoryScoreDict1
            subjectCategoryDict[fileName] = uniCategoryScoreDict

            sys.stdout.write(' Done!\n')
            counter += 1
            if not progressBar is None:
                progressBar.setValue(counter / totalFiles * 100)

        if singleFolder:
            destinationFile = destinationFolder + fs + 'Cumulative_Score_Results' + resultExt
        else:
            destinationFile = destinationFolder + fs + unicode(os.path.basename(os.path.dirname(dataFolder))) + '_Cumulative_Score_Results' + resultExt

        writeCsv(destinationFile, subjectCategoryDict, subjectResponseDict, sorted(fileNameList), sorted(uniCategoryList), sorted(idList),scoreTypeList,delimiter)
        sys.stdout.write('\nTotal process done!\n')
    if not progressBar is None:
        progressBar.setValue(100)


def showErrorMessage(self,message):
    """
    Shows about window
    """

    error ="Error"

    msgBox = QtGui.QMessageBox(self)
    #msgBox.setWindowIcon(self.about_icon)
    msgBox.about(msgBox,error,message)

def listDataFolders(dataDir):

    folderList = sorted(glob.glob(dataDir + fs + '*/'))

    return folderList


def listDataFiles(dataDir,extension):

    fileList     = sorted(glob.glob(dataDir + fs + '*' + extension))

    return fileList

def readCsv(pathToCsv):
    """
    Reads csv file to a list containing dictionaries, each representing a row.
    The keys of the dictionary represents the column names, and the value contains
    the corresponding value of that cell.

    Args:
        path_to_csv (string): a path to the csv file to be parsed
    Returns:
        a tuple containing a list with column names, and the rest of the data
        as a list of dictionaries

    """
    try:
        f_csv = codecs.open(pathToCsv,"rb", encoding='utf-8')
    except IOError as e:
        print >> sys.stderr, e
        return False

    # Try to determine which format of csv is used. In some countries, the
    # list separator symbol is ; instead of , and hopefully this will catch that
#    # discrepancy.
#    try:
#        dialect = csv.Sniffer().sniff(f_csv.readline())
#    except:
#        print >> sys.stderr, "Failed to sniff parameters for file {0}, assuming , to be the delimiter symbol".format(os.path.split(pathToCsv)[1])
#        dialect = csv.get_dialect('excel')
#
#    f_csv.seek(0)

    # Read the file with dictreader. If the file is empty or corrupt (such as defaultlog.csv in OpenSesame)
    # then skip the file but print an error message.
#    try:
    #data = csv.reader(f_csv,dialect=dialect)
    data = UnicodeReader(f_csv)
    rowDataList = list(data)
    headerList        = rowDataList[0]
    dataTupleList     = zip(*rowDataList[1:])


    boek = {}
    for index in range(len(headerList)):

        headerString =  headerList[index]
        dataTuple =  dataTupleList[index]

        ##unsanitize because the mc plugin has the U+XXXX notation for the response
        ## plugin is debugged

        dataTuple = tuple([unsanitize(x) for x in dataTuple])
        headerString = unsanitize(headerString)

        boek[headerString] = dataTuple


    return(boek)
#    except Exception as e:
#        print >> sys.stderr, "Failed to read file {0}: {1}".format(os.path.split(pathToCsv)[1],e)
#        return (False, False)

def writeCsv(pathToCsv, subjectCategoryDict, subjectResponseDict, dataFileList, uniCats, idList, scoreTypeList, delimiter):

    try:
        out_fp = codecs.open(pathToCsv,"wb", encoding='utf-8')
    except IOError as e:
        print >> sys.stderr, e
        return False

    #writer = csv.writer(out_fp, delimiter=delimiter)
    writer = UnicodeWriter(out_fp, delimiter=delimiter)


    catHeader = []
    for cat in uniCats:
        for _type in scoreTypeList:
            catHeader = catHeader + [unicode(cat) + '_' + _type]

    responseHeader = []
    for _id in idList:
        responseHeader = responseHeader + [_id]

    header = ['Item'] + catHeader + responseHeader
    writer.writerow(header)

    for dataFile in dataFileList:
        categoryDict = subjectCategoryDict[dataFile]
        score =[]
        for category in uniCats:
            scoreDict = categoryDict[category]

            for scoreType in scoreTypeList:
                score.append(scoreDict[scoreType])

        responseDict = subjectResponseDict[dataFile]
        responseList = []
        for _id in idList:
            responseList.append(responseDict[_id])

        row = [dataFile]  +  score + responseList
        writer.writerow(row)

    out_fp.close()

def unsanitize(s):

    """
    Converts the U+XXXX notation back to actual Unicode encoding

    Arguments:
    s -- a regular string to be unsanitized

    Returns:
    A unicode string with special characters
    """
    regexpUnsanitize = re.compile( r'U\+([A-F0-9]{4})')

    #s = unistr(s)
    while True:
        m = regexpUnsanitize.search(s)
        if m == None:
            break
        s = s.replace(m.group(0), unichr(int(m.group(1), 16)), 1)
    return s


def unistr(val):

        """
        desc: |
            Converts a value to a unicode string. This function is mostly
            necessary to make sure that normal strings with special characters
            are correctly encoded into unicode, and don't result in TypeErrors.

            The conversion logic is as follows:

            - unicode values are returned unchanged.
            - str values are decoded using utf-8.
            - all other types are typecast to unicode, assuming utf-8 encoding
              where applicable.

        arguments:
            val:
                desc:    A value of any type.

        returns:
            desc:    A unicode string.
            type:    unicode
        """
        encoding = u'utf-8'
        # Unicode strings cannot (and need not) be encoded again
        if isinstance(val, unicode):
            return val
        # Regular strings need to be encoded using the correct encoding
        if isinstance(val, str):
            return unicode(val, encoding=encoding, errors=u'replace')
        # Numeric values are encoded right away
        if isinstance(val, int) or isinstance(val, float):
            return unicode(val)
        # Some types need to be converted to unicode, but require the encoding
        # and errors parameters. Notable examples are Exceptions, which have
        # strange characters under some locales, such as French. It even appears
        # that, at least in some cases, they have to be encodeed to str first.
        # Presumably, there is a better way to do this, but for now this at
        # least gives sensible results.
        try:
            return unicode(str(val), encoding=encoding, errors=u'replace')
        except:
            pass
        # For other types, the unicode representation doesn't require a specific
        # encoding. This mostly applies to non-stringy things, such as integers.
        return unicode(val)



class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        #data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

