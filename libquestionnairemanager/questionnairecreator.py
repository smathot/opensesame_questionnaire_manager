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
#from __future__ import unicode_literals
import tarfile
import io
import codecs
import os


def QuestionnaireCreator(infile, fileName, name, resolutionHorizontal, resolutionVertical, bgcolor, fgcolor, backend, instruction, order, questions, _id, answers, category, score, type_):

    nrcycles = str(len(questions))

    stringList = []
    stringList.append(bgcolor)
    stringList.append(fgcolor)
    stringList.append(backend)
    stringList.append('custom')
    stringList.append(resolutionHorizontal)
    stringList.append(resolutionVertical)

    stringList.append(nrcycles)
    stringList.append(order)

    stringList.append(instruction.replace('\n','  <br />'))

    if type_ == 'mc':

        string9 = ''
        for index in range(len(questions)):
            string9 = string9 + '\tsetcycle '+str(index)+' category \"'+category[index]+'\"\n' \
                '\tsetcycle '+str(index)+' answer_options_scores "'+score[index]+'\"\n' \
                '\tsetcycle '+str(index)+' answer_options \"'+answers+'\"\n' \
                '\tsetcycle '+str(index)+' id \"'+_id[index]+'\"\n' \
                '\tsetcycle '+str(index)+' question_text "'+questions[index]+'\"'

            if index < len(questions)-1:
                string9 = string9 +'\n'
        stringList.append(string9)

        stringList.append(answers)


    if type_ == 'open':

        string9 = ''
        for index in range(len(questions)):
            string9 = string9 + '\tsetcycle '+str(index)+' id \"'+_id[index]+'\"\n' \
                '\tsetcycle '+str(index)+' question_text "'+questions[index]+'\"'

            if index < len(questions)-1:
                string9 = string9 +'\n'

        stringList.append(string9)



    replacementDict = {}
    for index in range(len(stringList)):
        replacementDict['@@'+str(index)+'@@'] = stringList[index]


    with open (infile, "r") as myfile:
        data=myfile.read()


    for src, target in replacementDict.iteritems():
         data = data.replace(src, target)

    scriptName = 'script.opensesame'

    cleanData = usanitize(data)

    tardata =   io.BytesIO(cleanData)

    tarinfo = tarfile.TarInfo(scriptName)
    tarinfo.size = len(cleanData)

    archive = tarfile.open(fileName, "w|gz")
    archive.addfile(tarinfo, tardata)


def usanitize(s):

    _s = codecs.encode(s, u'ascii', u'osreplace')
    _s = str(_s)
    return _s.replace(os.linesep, '\n')

def osreplace(exc):

	"""
	desc:
		A replacement function to allow opensame-style replacement of unicode
		characters.

	arguments:
		exc:
			type:	UnicodeEncodeError

	returns:
		desc:	A (replacement, end) tuple.
		type:	tuple
	"""

	_s = u''
	for ch in exc.object[exc.start:exc.end]:
		_s += u'U+%.4X' % ord(ch)
	return _s, exc.end

codecs.register_error(u'osreplace', osreplace)