#!/usr/bin/env python
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

import glob
from libquestionnairemanager import questionnairemanager_ui
from distutils.core import setup

setup(name="opensesame-questionnaire-manager",

	version = str(questionnairemanager_ui.version),
	description = "OpenSesame Questionnaire Manager can create, manage and process OpenSesame Questionnaires",
	author = "Bob Rosbag",
	author_email = "debian@bobrosbag.nl",
	url = "https://github.com/dev-jam/opensesame-questionnaire-manager",
	scripts = ["questionnaire-manager","questionnaire-processor"],
	packages = [ \
		"libquestionnairemanager", \
		],
	package_dir = { \
		"libquestionnairemanager" : "libquestionnairemanager", \
		},
	data_files=[
		("/usr/share/opensesame_questionnaire_manager", ["COPYING"]), \
		("/usr/share/applications", ["data/questionnaire-manager.desktop","data/questionnaire-processor.desktop"]), \
		("/usr/share/opensesame_questionnaire_manager/resources", \
			glob.glob("resources/*"),\
		("/usr/share/opensesame_questionnaire_manager/subjectmeasures", \
			glob.glob("subjectmeasures/*")),
		]
	)
