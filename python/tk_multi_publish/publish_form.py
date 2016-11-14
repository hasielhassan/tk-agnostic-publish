# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import traceback
from tank.platform.qt import QtCore, QtGui
from .task import Task

class PublishForm(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """

    # signals
    publish = QtCore.Signal()
    
    def __init__(self, app, handler, parent=None):
        """
        Construction
        """

        QtGui.QWidget.__init__(self, parent)

        self._app = app

        self._app._initialize = self._initialize
        
        # TODO: shouldn't need the handler
        self._handler = handler
    
        self._primary_task = None
        self._tasks = []
        
        # set up the UI
        from .ui.publish_form import Ui_PublishForm
        self._ui = Ui_PublishForm() 
        self._ui.setupUi(self)
        
        self._ui.publish_details.publish.connect(self._on_publish)
        self._ui.publish_details.cancel.connect(self._on_close)
        self._ui.publish_result.close.connect(self._on_close)
        
        expand_single_items = self._app.get_setting("expand_single_items")
        self._ui.publish_details.expand_single_items = expand_single_items
        
        allow_taskless_publishes = self._app.get_setting("allow_taskless_publishes")
        self._ui.publish_details.allow_no_task = allow_taskless_publishes
        
        self._ui.primary_error_label.setVisible(False)

        #config for dragable workfile
        self._ui.work_drag_area.setAcceptDrops(True)
        self._ui.work_drag_area.dragEnterEvent = self.dragEnterEvent
        self._ui.work_drag_area.dropEvent = self.dropEvent
        
        # always start with the details page:
        self.show_publish_details()
        
        # initialize:
        self._initialize()

    def dragEnterEvent(self, event):
        """
        """
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        """
        try:
            if event.mimeData().hasUrls:
                event.setDropAction(QtCore.Qt.CopyAction)
                event.accept()
                urls = event.mimeData().urls()
                if len(urls) == 1:

                    file_name = os.path.abspath(urls[0].toLocalFile())
                    droped_file_extension = os.path.splitext(file_name)[1][1:]

                    for output in self._handler._primary_outputs:
                        if output.extension == droped_file_extension:
                            self._handler._primary_output = output
                            self._app.agnostic_scene_contents['primary'] = {'type': 'primary', 'path': file_name, 'output': output}

                    if not self._app.agnostic_scene_contents['primary']:
                        QtGui.QMessageBox.warning(None, "File Warning!", "The file format (extension) you droped, don't match with any of the available ones declared on your environment!")

                    self._app.initialized_from = "primary"
                    self._initialize()
                    #self.update_workfile_details(file_name)

                else:
                    QtGui.QMessageBox.warning(None, "File Warning!", "You drop more that one file, try again!")
            else:
                event.ignore()
        except:
            QtGui.QMessageBox.warning(None, "Runtime Error!", traceback.format_exc())

        
    @property
    def selected_tasks(self):
        """
        The currently selected tasks
        """
        return self._get_selected_tasks()
    
    @property
    def shotgun_task(self):
        """
        The shotgun task that the publish should be linked to
        """
        return self._ui.publish_details.shotgun_task
        
    @property
    def thumbnail(self):
        """
        The thumbnail to use for the publish
        """
        return self._ui.publish_details.thumbnail
         
    @property
    def comment(self):
        """
        The comment to use for the publish
        """
        return self._ui.publish_details.comment
    
    def show_publish_details(self):
        self._ui.pages.setCurrentWidget(self._ui.publish_details)
        
    def show_publish_progress(self, title):
        self._ui.pages.setCurrentWidget(self._ui.publish_progress)
        self._ui.publish_progress.title = title
    
    def set_progress_reporter(self, reporter):
        self._ui.publish_progress.set_reporter(reporter)
        
    def show_publish_result(self, success, errors):
        """
        Show the result of the publish in the UI
        """
        # show page:
        self._ui.pages.setCurrentWidget(self._ui.publish_result)
        self._ui.publish_result.status = success
        self._ui.publish_result.errors = errors
        
    def _initialize(self):
        """
        Initialize UI with information provided
        """
        
        # pull initial data from handler:
        tasks = self._handler.get_publish_tasks()
        sg_tasks = self._handler.get_shotgun_tasks()
        thumbnail = self._handler.get_initial_thumbnail()
        sg_task = self._app.context.task
        
        # split tasks into primary and secondary:
        primary_task = None
        secondary_tasks = []
        for task in tasks:
            if task.output.is_primary:
                if primary_task:
                    # should never get this far but just in case!
                    raise Exception("Found multiple primary tasks - don't know how to handle this!")
                primary_task = task
            else:
                secondary_tasks.append(task)
                
        # initialize primary task UI:
        if primary_task:
            self._set_primary_task(primary_task)

        # initialize publish details form:
        self._ui.publish_details.initialize(secondary_tasks, sg_tasks)
        
        # set the initial thumbnail, comment and shotgun task
        self._ui.publish_details.comment = ""
        self._ui.publish_details.thumbnail = thumbnail
        self._ui.publish_details.shotgun_task = sg_task
        if sg_task:
            self._ui.publish_details.can_change_shotgun_task = False

         
    def _get_selected_tasks(self):
        """
        Get a list of the selected tasks that 
        should be published
        """
        
        # always publish primary task:
        selected_tasks = [self._primary_task]
        
        # get secondary tasks from details form:
        selected_tasks.extend(self._ui.publish_details.selected_tasks)
        
        return selected_tasks
        
    def _set_primary_task(self, task):
        """
        Set the primary task and update the UI accordingly
        """
        self._primary_task = task

        # connect to the primary tasks modified signal so that we can
        # update the UI if something changes.
        self._primary_task.modified.connect(self._on_primary_task_modified)
        
        # update UI for primary task:
        icon_path = self._primary_task.output.icon_path
        if os.path.isfile(icon_path) and os.path.exists(icon_path):
            icon = QtGui.QPixmap(icon_path)
            if not icon.isNull():
                self._ui.primary_icon_label.setPixmap(icon)
        
        # build details text and set:            
        lines = []
        name_str = self._primary_task.output.display_name
        if self._primary_task.item.name:
            name_str = "%s - %s" % (name_str, self._primary_task.item.name)
        lines.append("<span style='font-size: 16px'}><b>%s</b></span><span style='font-size: 12px'}>" % (name_str))
        if self._primary_task.output.description:
            lines.append("%s" % self._primary_task.output.description)
        if self._primary_task.item.description:
            lines.append("%s" % self._primary_task.item.description)
        details_txt = "%s</span>" % "<br>".join(lines) 
        self._ui.primary_details_label.setText(details_txt)
        
        # update errors text:
        self.__update_primary_errors()
        
    def _on_primary_task_modified(self):
        """
        Called when the primary task has been modified, e.g. there are new errors to report
        """
        # update the errors display for the primary publish
        self.__update_primary_errors()
        
    def __update_primary_errors(self):
        """
        Update the primary publish UI with any errors that were found during the pre-publish stage
        """
        if self._primary_task and self._primary_task.pre_publish_errors:
            error_txt = ("<font color='orange'>Validation checks returned some messages for your attention:"
                          "</font><br>%s" % "<br>".join(self._primary_task.pre_publish_errors))
            self._ui.primary_error_label.setText(error_txt)
            self._ui.primary_error_label.setVisible(True)
        else:
            self._ui.primary_error_label.setVisible(False)
        
        
    def _on_publish(self):
        """
        Slot called when the publish button in the dialog is clicked
        """
        self.publish.emit()
        
    def _on_close(self):
        """
        Slot called when the cancel or close signals in the dialog 
        are recieved
        """
        self.close()
        
        
        
        
        
        
        
        
        