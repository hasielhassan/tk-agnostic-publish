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

class PublishOutput(object):
    """
    Encapsulate an output definition as 
    loaded from the configuration
    """
    
    PRIMARY_NAME = "primary"
    
    def __init__(self, app, fields={}, name=None, selected=None, required=None):
        """
        Construction
        """
        self._app = app
        self._raw_fields = fields
        
        # special case handling of some fields that can be provided either
        # as args or through the fields
        self._name = (fields.get("name", "") if name == None else name)
        self._required = (fields.get("required", False) if required == None else required)
        self._selected = self._required or (fields.get("selected", True) if selected == None else selected)
        
    @property
    def name(self):
        return self._name    

    @property
    def scene_item_type(self):
        return self._raw_fields["scene_item_type"]
    
    @property
    def display_name(self):
        return self._raw_fields["display_name"]
    
    @property
    def display_group(self):
        return self._raw_fields.get("display_group", "")
    
    @property
    def description(self):
        return self._raw_fields["description"]
    
    @property
    def icon_path(self):
        return self._raw_fields["icon"]
    
    @property
    def tank_type(self):
        return self._raw_fields["tank_type"]
    
    @property
    def publish_template(self):
        return self._app.get_template_by_name(self._raw_fields["publish_template"])
        
    @property
    def selected(self):
        return self._selected
    
    @property
    def required(self):
        return self._required
    
    @property
    def is_primary(self):
        return self.name == PublishOutput.PRIMARY_NAME
    
    