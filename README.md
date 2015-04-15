OpenSesame Questionnaire Manager
==========
Copyright Bob Rosbag (2015)

ABOUT
-----
Current version: 1.0

OpenSesame Questionnaire Manager can create, manage and process OpenSesame Questionnaires


DOCUMENTATION AND INSTALLATION INSTRUCTIONS
-------------------------------------------
This is a standalone program that does not need to be installed. Make sure your 
python environment meets all dependencies specified below and that all files in
this repository are located in the same folder.

If you want to use the GUI simply run the program by

    python questionnaire-manager
    and/or
    python questionnaire-processor

It is also possible to use the program from CLI:

    python questionnaire-processor <source_folder> [<target_folder>]

To use the CLI method it is required the questionnaires originate from the OpenSesame Questionnaire Manager or contain the same column names in the log files


DEPENDENCIES
------------
- PyQt4 (QtGui, QtCore, uic) <http://www.riverbankcomputing.com/software/pyqt/download>
- NumPy <http://http://www.numpy.org>
- openpyxl <https://bitbucket.org/ericgazoni/openpyxl/wiki/Home>
