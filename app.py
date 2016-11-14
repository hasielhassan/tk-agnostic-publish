# Copyright (c) 2015 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Multi Publish

"""

import os
import tank
from tank import TankError

class MultiPublish(tank.platform.Application):

    def init_app(self):
        """
        Called as the application is being initialized
        """
        
        tk_multi_publish = self.import_module("tk_multi_publish")
        
        self._publish_handler = tk_multi_publish.PublishHandler(self)
        
        # register commands:
        display_name = self.get_setting("display_name")
        
        # "Publish Render" ---> publish_render
        command_name = display_name.lower().replace(" ", "_")
        if command_name.endswith("..."):
            command_name = command_name[:-3]
        params = {"short_name": command_name, 
                  "title": "%s..." % display_name,
                  "description": "Publishing of data into Shotgun"}
        
        self.engine.register_command("%s..." % display_name, 
                                     self._publish_handler.show_publish_dlg, 
                                     params)

    @property
    def context_change_allowed(self):
        """
        Specifies that context changes are allowed.
        """
        return True

    def destroy_app(self):
        self.log_debug("Destroying tk-multi-publish")
        
    def copy_file(self, source_path, target_path, task):
        """
        Utility method to copy a file from source_path to
        target_path.  Uses the copy file hook specified in 
        the configuration
        """
        self.execute_hook("hook_copy_file", 
                          source_path=source_path, 
                          target_path=target_path,
                          task=task)

    def post_context_change(self, old_context, new_context):
        """
        Runs after a context change has completed.

        :param old_context: The sgtk.context.Context being switched from.
        :param new_context: The sgtk.context.Context being switched to.
        """
        self._publish_handler.rebuild_primary_output()
