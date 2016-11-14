# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import time

import tank
from tank.platform.qt import QtCore, QtGui

class PublishProgressForm(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """
    
    def __init__(self, parent=None):
        """
        Construction
        
        :param parent:    The parent QWidget for this form
        """
        QtGui.QWidget.__init__(self, parent)
    
        self._reporter = None
        self.__title = "Doing Something"
        self.__current_stage = 1
        
        # set up the UI
        from .ui.publish_progress_form import Ui_PublishProgressForm
        self._ui = Ui_PublishProgressForm() 
        self._ui.setupUi(self)
        
        self._ui.progress_bar.setValue(0)
        self._ui.stage_progress_bar.setValue(0)
        self._ui.details.setText("")
        
    # title property
    # @property
    def __get_title(self):
        return self.__title
    # @title.setter
    def __set_title(self, value):
        self.__title = value
        self.__update_title(True)
    title=property(__get_title, __set_title)
    
    def set_reporter(self, reporter):
        """
        Connect to the reporter
        
        :param reporter:    The reporter instance to connect to
        """
        if self._reporter:
            self._reporter.progress.disconnect(self._on_progress)
        self._reporter = reporter
        if self._reporter:
            self._reporter.progress.connect(self._on_progress)
            self._ui.progress_bar.setVisible(self._reporter.stage_count > 1)
    
    def _on_progress(self, stage, stage_amount, total_amount, msg):
        """
        Progress event handler - responsible for updating the UI with the
        latest reported progress.
        
        :param stage:           The index of the current stage being processed
        :param stage_amount:    The progress for the current stage
        :param total_amount:    The overall progress
        :param msg:             Any message to report with the progress. 
        """
        # update the title:
        self.__current_stage = stage
        self.__update_title()
        
        # update the main progress bar:
        self._ui.progress_bar.setVisible(self._reporter.stage_count > 1)
        self._ui.progress_bar.setValue(total_amount)
        
        # update the stage progress bar:
        self._ui.stage_progress_bar.setValue(stage_amount)
        if msg != None:
            self._ui.details.setText(msg)

        # force Qt to process all events:
        QtCore.QCoreApplication.processEvents()

        # give Qt a chance to process any events!
        time.sleep(0.1)
        
    def __update_title(self, force_refresh=False):
        """
        Update the title to be "title (x of y)..." to more
        clearly indicate how far through the process things are
        
        :param force_refresh:    Force UI to refresh
        """
        # update the title:
        x_of_y = ""
        if self._reporter.stage_count > 1:
            x_of_y = " (%d of %d)" % (max(1, self.__current_stage), max(1, self._reporter.stage_count))
        title_str = "%s%s..." % (self.__title, x_of_y)
        self._ui.title.setText(title_str)
        
        # if need to, make sure all events are processed to refresh the UI:
        if force_refresh:
            QtCore.QCoreApplication.processEvents()
            time.sleep(0.1)
        
        
        