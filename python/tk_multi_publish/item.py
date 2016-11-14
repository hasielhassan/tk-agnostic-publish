# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

from sgtk import TankError

class Item(object):
    """
    Encapsulate an item returned by the scan hook
    """
    def __init__(self, fields={}):
        self._raw_fields = fields
    
    @property
    def raw_fields(self):
        return self._raw_fields
        
    @property
    def name(self):
        return self._raw_fields.get("name", "")
    
    @property
    def scene_item_type(self):
        return self._raw_fields["type"]

    @property
    def description(self):
        return self._raw_fields.get("description")
    
    @property
    def selected(self):
        return self.required or self._raw_fields.get("selected", True)

    @property
    def required(self):
        return self._raw_fields.get("required", False)
    
    def validate(self):
        required_keys = ["name", "type"]
        for rk in required_keys:
            if rk not in self._raw_fields.keys():
                raise TankError("Item does not contain required field '%s'" % rk)
    