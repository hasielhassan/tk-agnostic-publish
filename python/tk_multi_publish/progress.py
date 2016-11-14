# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

from tank.platform.qt import QtCore

class ProgressReporter(QtCore.QObject):
    """
    Simple progress interface
    """
    
    # signal emitted when new progress has been reported.
    progress = QtCore.Signal(int, float, float, object)# stage, stage_percent, overall_percent, message
    
    def __init__(self, stage_count=1):
        """
        Construction
        """
        QtCore.QObject.__init__(self)

        self._stage_count = stage_count
        self._stages = []
        
        self._current_stage = None
        self._previous_stage_percent = 0.0
        self._previous_percent = 0.0
        
    # @property
    def __get_stage_count(self):
        return self._stage_count   
    # @stage_count.setter
    def __set_stage_count(self, value):
        self._stage_count = max(1, value)
    stage_count=property(__get_stage_count, __set_stage_count)

    def reset(self, new_stage_count=None):
        self._stages = []
        if new_stage_count != None:
            self._stage_count = max(1, new_stage_count)
        self._current_stage = None
        self._previous_stage_percent = 0.0
        self._previous_percent = 0.0
        self.progress.emit(1, 0.0, 0.0, "")

    def report(self, percent, msg=None, stage=None):
        """
        Used to report progress.
        """
        if not stage:
            # progress is being reported for the previous stage:
            stage = self._current_stage
        else:
            # keep track of the stages that have been reported:
            found_stage = False
            for s in self._stages:
                if s == stage:
                    found_stage = True
                    break
            if not found_stage:
                # this is a new stage
                self._stages.append(stage)
                self._previous_stage_percent = 0.0
            else:
                # TODO - this currently doesn't handle reporting progress 
                # asynchronously across stages!
                pass

        # clamp the stage percentage and stop it going backwards!:
        stage_percent = min(max(percent, 0.0), 100.0)
        if stage_percent < self._previous_stage_percent:
            stage_percent = self._previous_stage_percent
        
        # work out per-stage percentage based on the number of stages
        stage_num = max(1, len(self._stages))
        max_stage_count = max(self._stage_count, stage_num)
        
        # work out the current overall percentage.  This
        # will depend on the number of stages completed
        # so far
        current_percent = ((100.0 * (stage_num-1)) + stage_percent)/max_stage_count
        
        # just in case, clamp and stop it going backwards!:
        current_percent = min(max(current_percent, 0.0), 100.0)
        if current_percent < self._previous_percent:
            current_percent = self._previous_percent
        
        # emit signal:
        try:
            self.progress.emit(stage_num, stage_percent, current_percent, msg)
        finally:
            self._current_stage = stage
            self._previous_stage_percent = stage_percent
            self._previous_percent = current_percent
        
class TaskProgressReporter(ProgressReporter):
    def __init__(self, tasks):
        ProgressReporter.__init__(self, len(tasks))
        
        # build task index for tasks:
        self._task_index = {}
        for task in tasks:
            self._task_index[(task.item.name, task.output.name)] = task
        
    def report(self, percent, msg=None, stage=None):

        if not stage:
            # progress is being reported for the previous stage:
            stage = self._current_stage

        # if stage matches a task then we want to include
        # the task details at the start of the message:
        if msg != None:        
            try:
                item_name = stage["item"]["name"]
                output_name = stage["output"]["name"]
                
                # find task that matches:
                task = self._task_index.get((item_name, output_name))
                
                if task:
                    # update message to include task info:
                    msg = "%s - %s: %s" % (task.output.display_name, task.item.name, msg)
            except:
                pass
        
        # call base class:
        ProgressReporter.report(self, percent, msg, stage)
            
            
            
        
        
        