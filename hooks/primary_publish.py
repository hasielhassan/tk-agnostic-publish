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
import uuid
import tempfile
import traceback

import tank
from tank import Hook
from tank import TankError
from tank.platform.qt import QtCore, QtGui

class PrimaryPublishHook(Hook):
    """
    Single hook that implements publish of the primary task
    """    
    def execute(
        self, task, work_template, comment, thumbnail_path, sg_task, progress_cb,
        user_data, **kwargs):
        """
        Main hook entry point
        :param task:            Primary task to be published.  This is a
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
               
        :param comment:         String
                                The comment provided for the publish
                        
        :param thumbnail:       Path string
                                The default thumbnail provided for the publish
                        
        :param sg_task:         Dictionary (shotgun entity description)
                                The shotgun task to use for the publish    
                        
        :param progress_cb:     Function
                                A progress callback to log progress during pre-publish.  Call:
                                
                                    progress_cb(percentage, msg)
                                     
                                to report progress to the UI

        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.
        
        :returns:               Path String
                                Hook should return the path of the primary publish so that it
                                can be passed as a dependency to all secondary publishes
                
        :raises:                Hook should raise a TankError if publish of the 
                                primary task fails
        """
        # get the engine name from the parent object (app/engine/etc.)
        engine = self.parent.engine
        engine_name = engine.name
        args = [
            task,
            work_template,
            comment,
            thumbnail_path,
            sg_task,
            progress_cb,
            user_data
        ]

        self.parent.log_debug("Ready to run publish")
        
        return self._do_publish(*args)


    def _do_publish(
        self, task, work_template, comment, thumbnail_path, sg_task,
        progress_cb, user_data):
        """
        Publish the main scene

        :param task:            The primary task to publish
        :param work_template:   The primary work template to use
        :param comment:         The publish description/comment
        :param thumbnail_path:  The path to the thumbnail to associate with the published file
        :param sg_task:         The Shotgun task that this publish should be associated with
        :param progress_cb:     A callback to use when reporting any progress
                                to the UI
        :param user_data:       A dictionary containing any data shared by other hooks run prior to
                                this hook. Additional data may be added to this dictionary that will
                                then be accessible from user_data in any hooks run after this one.

        :returns:               The path to the file that has been published        
        """
        try:
            progress_cb(0.0, "Finding scene dependencies", task)
            dependencies = self._find_additional_scene_dependencies()
            
            # get scene path
            scene_path = task['item']['other_params']['source']
            publish_path = task['item']['other_params']['destination']
            publish_template = task["output"]["publish_template"]
            fields = publish_template.get_fields(publish_path)

            # copy the file:
            progress_cb(50.0, "Copying the file")
            try:
                publish_folder = os.path.dirname(publish_path)
                self.parent.ensure_folder_exists(publish_folder)
                self.parent.log_debug("Copying %s --> %s..." % (scene_path, publish_path))
                self.parent.copy_file(scene_path, publish_path, task)
            except Exception, e:
                raise TankError("Failed to copy file from %s to %s - %s" % (scene_path, publish_path, e))

            # work out publish name:
            publish_name = self._get_publish_name(publish_path, publish_template, fields)

            # finally, register the publish:
            progress_cb(75.0, "Registering the publish")
            self._register_publish(publish_path, 
                                   publish_name, 
                                   sg_task, 
                                   fields["version"], 
                                   task["output"]["tank_type"],
                                   comment,
                                   thumbnail_path, 
                                   dependencies)
            
            progress_cb(100)
        except:
            QtGui.QMessageBox.warning(None, "Runtime Error!", traceback.format_exc())
        
        return publish_path

    def _find_additional_scene_dependencies(self):
        """
        Find additional dependencies from the scene
        """
        # default implementation does nothing!
        return []
    
    def _get_publish_name(self, path, template, fields=None):
        """
        Return the 'name' to be used for the file - if possible
        this will return a 'versionless' name
        """
        # first, extract the fields from the path using the template:
        fields = fields.copy() if fields else template.get_fields(path)
        if "name" in fields and fields["name"]:
            # well, that was easy!
            name = fields["name"]
        else:
            # find out if version is used in the file name:
            template_name, _ = os.path.splitext(os.path.basename(template.definition))
            version_in_name = "{version}" in template_name
        
            # extract the file name from the path:
            name, _ = os.path.splitext(os.path.basename(path))
            delims_str = "_-. "
            if version_in_name:
                # looks like version is part of the file name so we        
                # need to isolate it so that we can remove it safely.  
                # First, find a dummy version whose string representation
                # doesn't exist in the name string
                version_key = template.keys["version"]
                dummy_version = 9876
                while True:
                    test_str = version_key.str_from_value(dummy_version)
                    if test_str not in name:
                        break
                    dummy_version += 1
                
                # now use this dummy version and rebuild the path
                fields["version"] = dummy_version
                path = template.apply_fields(fields)
                name, _ = os.path.splitext(os.path.basename(path))
                
                # we can now locate the version in the name and remove it
                dummy_version_str = version_key.str_from_value(dummy_version)
                
                v_pos = name.find(dummy_version_str)
                # remove any preceeding 'v'
                pre_v_str = name[:v_pos].rstrip("v")
                post_v_str = name[v_pos + len(dummy_version_str):]
                
                if (pre_v_str and post_v_str 
                    and pre_v_str[-1] in delims_str 
                    and post_v_str[0] in delims_str):
                    # only want one delimiter - strip the second one:
                    post_v_str = post_v_str.lstrip(delims_str)

                versionless_name = pre_v_str + post_v_str
                versionless_name = versionless_name.strip(delims_str)
                
                if versionless_name:
                    # great - lets use this!
                    name = versionless_name
                else: 
                    # likely that version is only thing in the name so 
                    # instead, replace the dummy version with #'s:
                    zero_version_str = version_key.str_from_value(0)        
                    new_version_str = "#" * len(zero_version_str)
                    name = name.replace(dummy_version_str, new_version_str)
        
        return name     
     

    def _register_publish(self, path, name, sg_task, publish_version, tank_type, comment, thumbnail_path, dependency_paths):
        """
        Helper method to register publish using the 
        specified publish info.
        """
        # construct args:
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": comment,
            "path": path,
            "name": name,
            "version_number": publish_version,
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "dependency_paths": dependency_paths,
            "published_file_type":tank_type,
        }
        
        self.parent.log_debug("Register publish in shotgun: %s" % str(args))
        
        # register publish;
        sg_data = tank.util.register_publish(**args)
        
        return sg_data
