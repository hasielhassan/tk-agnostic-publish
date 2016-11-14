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
import sys

import tank
from tank import Hook
from tank import TankError

class PostPublishHook(Hook):
    """
    Single hook that implements post-publish functionality
    """    
    def execute(
        self, work_template, primary_task, secondary_tasks, progress_cb,
        user_data, **kwargs
    ):
        """
        Main hook entry point
        
        :param work_template:   template
                                This is the template defined in the config that
                                represents the current work file

        :param primary_task:    The primary task that was published by the primary publish hook.  Passed
                                in here for reference.

        :param secondary_tasks: The list of secondary taskd that were published by the secondary 
                                publish hook.  Passed in here for reference.
                        
        :param progress_cb:     Function
                                A progress callback to log progress during pre-publish.  Call:
                        
                                    progress_cb(percentage, msg)
                             
                                to report progress to the UI

        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.

        :returns:               None
        :raises:                Raise a TankError to notify the user of a problem
        """
        # get the engine name from the parent object (app/engine/etc.)
        engine = self.parent.engine
        engine_name = engine.name

        self._do_post_publish(work_template, progress_cb, user_data)

    def _do_post_publish(self, work_template, progress_cb, user_data):
        """
        Do any post-publish work

        :param work_template:   The primary work template used for the publish
        :param progress_cb:     Callback to be used when reporting progress
        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.
        """        
        
        progress_cb(0, "Doing Post-Publish")

        #default implementation do nothing        
        
        progress_cb(100)
 
    def _get_next_work_file_version(self, work_template, fields):
        """
        Find the next available version for the specified work_file
        """
        existing_versions = self.parent.tank.paths_from_template(work_template, fields, ["version"])
        version_numbers = [work_template.get_fields(v).get("version") for v in existing_versions]
        curr_v_no = fields["version"]
        max_v_no = max(version_numbers)
        return max(curr_v_no, max_v_no) + 1





        
        
