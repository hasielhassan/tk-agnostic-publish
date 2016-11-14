# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank
from tank.platform.qt import QtCore, QtGui

from group_header import GroupHeader
from output_item import OutputItem
from item_list import ItemList
from error_list import ErrorList

thumbnail_widget = tank.platform.import_framework("tk-framework-widget", "thumbnail_widget")


class ThumbnailWidget(thumbnail_widget.ThumbnailWidget):
    pass


class _ObjWrapper(object):
    """ Wrap a python object for storage in PyQt and PySide items """
    def __init__(self, obj=None):
        self._obj = obj

    @property
    def obj(self):
        return self._obj


class PublishDetailsForm(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """

    # signals
    publish = QtCore.Signal()
    cancel = QtCore.Signal()
    
    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.expand_single_items = False
        self.allow_no_task = False
        
        self._group_widget_info = {}
        self._tasks = []
    
        # set up the UI
        from .ui.publish_details_form import Ui_PublishDetailsForm
        self._ui = Ui_PublishDetailsForm() 
        self._ui.setupUi(self)
        
        # create vbox layout for scroll widget:
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(2,2,2,2)
        self._ui.task_scroll.widget().setLayout(layout)
        
        # hook up buttons
        self._ui.publish_btn.clicked.connect(self._on_publish)
        self._ui.cancel_btn.clicked.connect(self._on_cancel)
        
        self.can_change_shotgun_task = True

    @property
    def selected_tasks(self):
        return self._get_selected_tasks()

    # @property
    def __get_shotgun_task(self):
        return self._get_sg_task_combo_task(self._ui.sg_task_combo.currentIndex())
    # @shotgun_task.setter
    def __set_shotgun_task(self, value):
        self._set_current_shotgun_task(value)
    shotgun_task=property(__get_shotgun_task, __set_shotgun_task)
    
    # @property
    def __get_comment(self):
        return self._safe_to_string(self._ui.comments_edit.toPlainText()).strip()
    # @comment.setter
    def __set_comment(self, value):
        self._ui.comments_edit.setPlainText(value)
    comment=property(__get_comment, __set_comment)

    # @property
    def __get_thumbnail(self):
        return self._ui.thumbnail_widget.thumbnail
    # @thumbnail.setter
    def __set_thumbnail(self, value):
        self._ui.thumbnail_widget.thumbnail = value
    thumbnail=property(__get_thumbnail, __set_thumbnail)
        
    # @property
    def __get_can_change_shotgun_task(self):
        """
        Control if the shotgun task can be changed or not
        """
        return self._ui.sg_task_stacked_widget.currenWidget() == self._ui.sg_task_menu_page
    # @can_change_shotgun_task.setter
    def __set_can_change_shotgun_task(self, value):
        page = None
        header_txt = ""
        if value:
            page = self._ui.sg_task_menu_page
            header_txt = "What Shotgun Task are you working on?"
        else:
            page = self._ui.sg_task_label_page
            header_txt = "The Publish will be associated with Shotgun Task:"

        self._ui.sg_task_stacked_widget.setCurrentWidget(page)
        self._ui.task_header_label.setText(header_txt)
    can_change_shotgun_task=property(__get_can_change_shotgun_task, __set_can_change_shotgun_task)
                    
    def initialize(self, tasks, sg_tasks):
        """
        Initialize UI
        """
        # reset UI to default state:
        self._ui.sg_task_combo.setEnabled(True)
        
        # populate shotgun task list:
        self._populate_shotgun_tasks(sg_tasks)
        
        # connect up modified signal on tasks:
        self._tasks = tasks

        # populate outputs list:
        self._populate_task_list()

    def _get_sg_task_combo_task(self, index):
        """
        Get the shotgun task for the currently selected item in the task combo
        """
        task = self._ui.sg_task_combo.itemData(index) if index >= 0 else None
        if task:
            if hasattr(QtCore, "QVariant") and isinstance(task, QtCore.QVariant):
                task = task.toPyObject()

            # task is a wrapped object to avoid PyQt QString conversion fun!
            if task:
                task = task.obj

        return task

    def _populate_shotgun_tasks(self, sg_tasks):
        """
        Populate the shotgun task combo box with the provided
        list of shotgun tasks
        """
        current_task = self._get_sg_task_combo_task(self._ui.sg_task_combo.currentIndex())
        self._ui.sg_task_combo.clear()
        
        # add 'no task' task:
        if self.allow_no_task:
            self._ui.sg_task_combo.addItem("Do not associate this publish with a task")
            self._ui.sg_task_combo.insertSeparator(self._ui.sg_task_combo.count())
            self._ui.sg_task_combo.insertSeparator(self._ui.sg_task_combo.count())
        
        # add tasks:
        for task in sg_tasks:
            label = "%s, %s" % (task["step"]["name"], task["content"])
            self._ui.sg_task_combo.addItem(label, _ObjWrapper(task))

        # reselect selected task if it is still in list:
        self._set_current_shotgun_task(current_task)
        
    def _set_current_shotgun_task(self, task):
        """
        Select the specified task in the shotgun task
        combo box
        """
        
        # update the selection combo:
        found_index = None
        for ii in range(0, self._ui.sg_task_combo.count()):
            item_task = self._get_sg_task_combo_task(ii)
            
            found = False
            if not task:
                found = not item_task
            elif item_task:
                found = task["id"] == item_task["id"]
            
            if found:
                found_index = ii
                break
        self._ui.sg_task_combo.setCurrentIndex(found_index or 0)
        
        # also update the static label:
        label = "None!"
        if found_index != None:
            label = self._ui.sg_task_combo.itemText(found_index)
        self._ui.sg_task_label.setText(label)
            
    def _populate_task_list(self):
        """
        Build the main task list for selection of outputs, items, etc.
        """
        
        # clear existing widgets:
        task_scroll_widget = self._ui.task_scroll.widget()
        self._group_widget_info = {}
        #TODO
        
        if len(self._tasks) == 0:
            # no tasks so show no tasks text:
            self._ui.publishes_stacked_widget.setCurrentWidget(self._ui.no_publishes_page)
            return
        else:
            self._ui.publishes_stacked_widget.setCurrentWidget(self._ui.publishes_page)
        
        # group tasks by display group:
        group_order = []
        tasks_by_group = {}
        for task in self._tasks:
            group = tasks_by_group.setdefault(task.output.display_group, dict())
            
            # track unique outputs for this group maintaining order
            # respective to task
            group_outputs = group.setdefault("outputs", list())
            if task.output not in group_outputs:
                group_outputs.append(task.output)
            
            # track unique items for this group maintaining order
            # respective to task
            group_items = group.setdefault("items", list())
            if task.item not in group_items:
                group_items.append(task.item)
            
            # track tasks for this group:
            group.setdefault("tasks", list()).append(task)

            if not task.output.display_group in group_order:
                group_order.append(task.output.display_group)            
        
        # add widgets to scroll area:
        layout = task_scroll_widget.layout()
        for group in group_order:
            
            widget_info = {}
            
            # add header:
            header = GroupHeader(group, task_scroll_widget)
            layout.addWidget(header)
            widget_info["header"] = header
        
            # add output items:
            output_widgets = []
            for output in tasks_by_group[group]["outputs"]:
                item = OutputItem(output, task_scroll_widget)
                layout.addWidget(item)
                output_widgets.append(item)
            widget_info["output_widgets"] = output_widgets

            # add item list if more than one item:                
            if self.expand_single_items or len(tasks_by_group[group]["items"]) > 1:
                item_list = ItemList(tasks_by_group[group]["items"], task_scroll_widget)
                layout.addWidget(item_list)
                widget_info["item_list"] = item_list
                
            # always add error list:
            error_list = ErrorList(tasks_by_group[group]["tasks"], task_scroll_widget)
            #error_list.setVisible(False)
            layout.addWidget(error_list)
            widget_info["error_list"] = error_list
            
            self._group_widget_info[group] = widget_info
                
        # add vertical stretch:
        layout.addStretch(1)
        
    def _get_selected_tasks(self):
        """
        Get the selected tasks from the UI
        """
        selected_tasks = []
        
        # build some indexes:
        task_index = {}
        tasks_per_output = {}
        for task in self._tasks:
            key = (task.output, task.item)
            if key in task_index.keys():
                raise "Didn't expect to find the same task in the list twice!"
            task_index[key] = task
            tasks_per_output.setdefault(task.output, list()).append(task)
        
        for info in self._group_widget_info.values():
            
            # go through output widgets
            for output_widget in info["output_widgets"]:
                if not output_widget.selected:
                    continue
                
                output = output_widget.output
                
                # go through item widgets:
                item_list = info.get("item_list")
                if item_list:
                    for item in item_list.selected_items:
                        task = task_index.get((output, item))
                        if task:
                            selected_tasks.append(task)
                else:
                    # assume all items for this output are selected:
                    tasks = tasks_per_output.get(output)
                    if tasks:
                        selected_tasks.extend(tasks)
            
        # finally, ensure that tasks are returned in their
        # original order:
        ordered_selected_tasks = [task for task in self._tasks if task in selected_tasks]
        return ordered_selected_tasks
                            
    def _on_publish(self):
        self.publish.emit()
        
    def _on_cancel(self):
        self.cancel.emit()
        
    def _safe_to_string(self, value):
        """
        safely convert the value to a string - handles
        QtCore.QString if usign PyQt
        """
        #
        if isinstance(value, basestring):
            # it's a string anyway so just return
            return value
        
        if hasattr(QtCore, "QString"):
            # running PyQt!
            if isinstance(value, QtCore.QString):
                # QtCore.QString inherits from str but supports 
                # unicode, go figure!  Lets play safe and return
                # a utf-8 string
                return str(value.toUtf8())
        
        # For everything else, just return as string
        return str(value)
        
        
        
        
        
        
        
        
      
