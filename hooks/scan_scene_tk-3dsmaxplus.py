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

import MaxPlus

import sgtk
from sgtk import Hook
from sgtk import TankError


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

        # get the main scene:
        filename = MaxPlus.FileManager.GetFileName()
        if not filename:
            raise TankError("Please Save your file before Publishing")

        # create the primary item - 'type' should match the 'primary_scene_item_type':
        items.append({"type": "work_file", "name": filename})

        # If there are objects in the scene, then we will register
        # a geometry item. This is a bit simplistic in it's approach
        # to determining whether there's exportable data in the scene
        # that's useful when exported as an Alembic cache, but it will
        # work in most cases.
        if list(MaxPlus.Core.GetRootNode().Children):
            items.append({"type": "geometry", "name": "All Scene Geometry"})

        return items



