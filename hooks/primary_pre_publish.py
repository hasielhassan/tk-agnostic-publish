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
from tank.platform.qt import QtCore, QtGui

class PrimaryPrePublishHook(Hook):
    """
    Single hook that implements pre-publish of the primary task
    """    
    def execute(self, task, work_template, progress_cb, user_data, **kwargs):
        """
        Main hook entry point
        :param task:            Primary task to be pre-published.  This is a
                                dictionary containing the following keys:
                                {   
                                    item:   Dictionary
                                            This is the item returned by the scan hook 
                                            {   
                                                name:           String
                                                description:    String
                                                type:           String
                                                other_params:   Dictionary
                                            }
                                           
                                    output: Dictionary
                                            This is the output as defined in the configuration - the 
                                            primary output will always be named 'primary' 
                                            {
                                                name:             String
                                                publish_template: template
                                                tank_type:        String
                                            }
                                }
        :param work_template:   template
                                This is the template defined in the config that
                                represents the current work file
                        
        :param progress_cb:     Function
                                A progress callback to log progress during pre-publish.  Call:
                        
                                    progress_cb(percentage, msg)
                             
                                to report progress to the UI

        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.

        :returns:               List 
                                A list of non-critical problems that should be 
                                reported to the user but not stop the publish.
                        
        :raises:                Hook should raise a TankError if the primary task
                                can't be published!
        """
        # get the engine name from the parent object (app/engine/etc.)
        engine = self.parent.engine
        engine_name = engine.name
        
        return self._do_pre_publish(task, work_template, progress_cb, user_data)


        
    def _do_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do primary pre-publish/scene validation

        :param task:            The primary task to pre-publish
        :param work_template:   The primary work template to use
        :param progress_cb:     A callback to use when reporting any progress
                                to the UI
        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.

        :returns:               A list of any errors or problems that were found
                                during pre-publish
        """
        
        progress_cb(0.0, "Validating current scene", task)
            
        # validate it:
        #scene_errors = self._validate_work_file(scene_path, work_template, task["output"], progress_cb)
        scene_errors = []

        if not os.path.exists(task['item']['other_params']['source']):
            scene_errors.append("The file (%s) not longer exists on disk!" % task['item']['other_params']['source'])
        
        progress_cb(100, "Pre publish ready")
        
        self.parent.log_debug("Returning prepublish: %s" % scene_errors)

        return scene_errors


    def _validate_work_file(self, path, work_template, output, progress_cb):
        """
        Validate that the given path is a valid work file and that
        the published version of it doesn't already exist.
        
        Return the new version number that the scene should be
        up'd to after publish
        """
        errors = []
        
        progress_cb(25, "Validating work file")
        
        if not work_template.validate(path):
            raise TankError("File '%s' is not a valid work path, unable to publish!" % path)
        
        progress_cb(50, "Validating publish path")
        
        # find the publish path:
        fields = work_template.get_fields(path)
        fields["TankType"] = output["tank_type"]
        publish_template = output["publish_template"]
        publish_path = publish_template.apply_fields(fields) 
        
        if os.path.exists(publish_path):
            raise TankError("A published file named '%s' already exists!" % publish_path)
        
        progress_cb(75, "Validating current version")
        
        # check the version number against existing work file versions to avoid accidentally
        # bypassing more recent work!
        existing_versions = self.parent.tank.paths_from_template(work_template, fields, ["version"])
        version_numbers = [ work_template.get_fields(v).get("version") for v in existing_versions]
        curr_v_no = fields["version"]
        max_v_no = max(version_numbers)
        if max_v_no > curr_v_no:
            # there is a higher version number - this means that someone is working
            # on an old version of the file. Warn them about upgrading.
            errors.append("Your current work file is v%03d, however a more recent version (v%03d) already exists.  "
                          "After publishing, this file will become v%03d, replacing any more recent work from v%03d!"
                          % (curr_v_no, max_v_no, max_v_no + 1, max_v_no))
        
        return errors
        
