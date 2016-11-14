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

import tank
from tank import Hook
from tank import TankError

import win32com
from win32com.client import Dispatch, constants
from pywintypes import com_error
Application = Dispatch("XSI.Application").Application

class ScanSceneHook(Hook):
    """
    Hook to scan scene for items to publish
    """
    
    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       A list of any items that were found to be published.  
                        Each item in the list should be a dictionary containing 
                        the following keys:
                        {
                            type:   String
                                    This should match a scene_item_type defined in
                                    one of the outputs in the configuration and is 
                                    used to determine the outputs that should be 
                                    published for the item
                                    
                            name:   String
                                    Name to use for the item in the UI
                            
                            description:    String
                                            Description of the item to use in the UI
                                            
                            selected:       Bool
                                            Initial selected state of item in the UI.  
                                            Items are selected by default.
                                            
                            required:       Bool
                                            Required state of item in the UI.  If True then
                                            item will not be deselectable.  Items are not
                                            required by default.
                                            
                            other_params:   Dictionary
                                            Optional dictionary that will be passed to the
                                            pre-publish and publish hooks
                        }
        """   
                
        items = []
        
        # query the current scene 'name' from the application:
        scene_name = Application.ActiveProject.ActiveScene.Name
                    
        # There doesn't seem to be an easy way to determin if the current scene 
        # is 'new'.  However, if the file name is "Untitled.scn" and the scene 
        # name is "Scene" rather than "Untitled", then we can be reasonably sure 
        # that we haven't opened a file called Untitled.scn
        scene_filepath = Application.ActiveProject.ActiveScene.filename.value
        if scene_name == "Scene" and os.path.basename(scene_filepath) == "Untitled.scn":
            raise TankError("Please Save your file before Publishing")

        # create the primary item - this will match the primary output 'scene_item_type':            
        items.append({"type": "work_file", "name": scene_name})

        return items
