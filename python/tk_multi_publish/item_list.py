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

class ItemWidget(QtGui.QWidget):
    """
    """
    def __init__(self, item, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        self._item = item
    
        # set up the UI
        from .ui.item import Ui_Item
        self._ui = Ui_Item() 
        self._ui.setupUi(self)
        
        # update selected state:
        self._ui.select_cb.setChecked(item.selected)
        self._ui.select_cb.setEnabled(not item.required)        
        
        # update description
        lines = []
        lines.append("<b>%s</b>" % self._item.name)
        if self._item.description:
            lines.append("%s" % self._item.description)
        self._ui.details_label.setText("<br>".join(lines))
        
    @property
    def item(self):
        return self._item
    
    @property
    def selected(self):
        return self._ui.select_cb.isChecked()
        
    def mousePressEvent(self, event):
        if self._ui.select_cb.isEnabled():
            self._ui.select_cb.setChecked(not self._ui.select_cb.isChecked())

        
        
class ItemList(QtGui.QWidget):
    """
    """
    def __init__(self, items, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
    
        self._items = items
        self._item_widgets = []
    
        self._is_collapsed = False
    
        # set up the UI
        from .ui.item_list import Ui_ItemList
        self._ui = Ui_ItemList() 
        self._ui.setupUi(self)
        
        # add a layout:
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(2,2,2,2)
        self._ui.item_frame.setLayout(layout)
        
        # add item widgets
        self._update_ui()
        
        # collapse by default:
        self._set_collapsed(True)
        
    @property
    def selected_items(self):
        return self._get_selected_items()
        
    # @property
    def __get_collapsed(self):
        return self._is_collapsed
    # @collapsed.setter
    def __set_collapsed(self, value):
        self._set_collapsed(value)
    collapsed=property(__get_collapsed, __set_collapsed)
        
    def mousePressEvent(self, event):
        """
        Event triggered on mouse press - if mouse
        is in header then this will toggle the collapsed
        state of the control
        """
        clicked_header = True
        if self._ui.line.isVisible():
            clicked_header = event.pos().y() < self._ui.line.y()
            
        if clicked_header:
            self._set_collapsed(not self._is_collapsed)
        
    def _set_collapsed(self, collapse):
        """
        Set collapsed state of the control
        """
        # show controls
        self._ui.item_frame.setVisible(not collapse)
        self._ui.line.setVisible(not collapse)
        
        # set icon:
        self._ui.expand_label.setPixmap([QtGui.QPixmap(":/res/group_collapse.png"), QtGui.QPixmap(":/res/group_expand.png")][collapse])
        
        self._is_collapsed = collapse
        
    def _update_ui(self):
        """
        Update UI
        """
        
        layout = self._ui.item_frame.layout()
        
        # first, clear all controls from item
        """
        for control in self._item_controls:
            control.setParent(None)
            control.deleteLater()
        self._item_controls.clear()
        """
        self._item_widgets = []
        
        # update title:
        num_items = len(self._items)
        title = ("<b>%d %s available</b>, <i>expand to turn individual items on and off</i>" 
                    % (num_items, ("item" if num_items == 1 else "items")))
        self._ui.section_label.setText(title)
        
        # now build widgets for list:
        
        for item in self._items:
            item_widget = ItemWidget(item, self._ui.item_frame)
            layout.addWidget(item_widget)
            
            self._item_widgets.append(item_widget)
            
    def _get_selected_items(self):
        """
        Return list of the selected items
        """
        selected_items = []
        for widget in self._item_widgets:
            if widget.selected:
                selected_items.append(widget.item)
        return selected_items    
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
