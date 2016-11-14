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
import shutil
import nuke

import tank
from tank import Hook
from tank import TankError

class PublishHook(Hook):
    """
    Single hook that implements publish functionality for secondary tasks
    """
    def __init__(self, *args, **kwargs):
        """
        Construction
        """
        # call base init
        Hook.__init__(self, *args, **kwargs)
        
        # cache a couple of apps that we may need later on:
        self.__write_node_app = self.parent.engine.apps.get("tk-nuke-writenode")
        self.__review_submission_app = self.parent.engine.apps.get("tk-multi-reviewsubmission")

    def execute(self, *args, **kwargs):
        """
        Main hook entry point
        :param tasks:                   List of secondary tasks to be published.  Each task is a 
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
                        
        :param work_template:           template
                                        This is the template defined in the config that
                                        represents the current work file
               
        :param comment:                 String
                                        The comment provided for the publish
                        
        :param thumbnail:               Path string
                                        The default thumbnail provided for the publish
                        
        :param sg_task:                 Dictionary (shotgun entity description)
                                        The shotgun task to use for the publish    
                        
        :param primary_publish_path:    Path string
                                        This is the path of the primary published file as returned
                                        by the primary publish hook
                        
        :param progress_cb:             Function
                                        A progress callback to log progress during pre-publish.  Call:
                                        
                                            progress_cb(percentage, msg)
                                             
                                        to report progress to the UI
                        
        :param primary_task:            The primary task that was published by the primary publish hook.  Passed
                                        in here for reference.  This is a dictionary in the same format as the
                                        secondary tasks above.

        :param user_data:               A dictionary containing any data shared by other hooks run prior to
                                        this hook. Additional data may be added to this dictionary that will
                                        then be accessible from user_data in any hooks run after this one.
        
        :returns:                       A list of any tasks that had problems that need to be reported 
                                        in the UI.  Each item in the list should be a dictionary containing 
                                        the following keys:
                                        {
                                            task:   Dictionary
                                                    This is the task that was passed into the hook and
                                                    should not be modified
                                                    {
                                                        item:...
                                                        output:...
                                                    }
                                                    
                                            errors: List
                                                    A list of error messages (strings) to report    
                                        }
        """
        engine = self.parent.engine
        if hasattr(engine, "hiero_enabled") and engine.hiero_enabled:
            return self._hiero_execute(*args, **kwargs)
        elif hasattr(engine, "studio_enabled") and engine.studio_enabled:
            return self._studio_execute(*args, **kwargs)
        else:
            return self._nuke_execute(*args, **kwargs)

    def _studio_execute(
        self, tasks, work_template, comment, thumbnail_path, sg_task,
        primary_task, primary_publish_path, progress_cb, **kwargs
    ):
        """
        The Nuke Studio specific secondary publish routine.
        """
        # We treat Nuke Studio the same as Hiero, so call through.
        return self._hiero_execute(
            tasks,
            work_template,
            comment,
            thumbnail_path,
            sg_task,
            primary_task,
            primary_publish_path,
            progress_cb,
            **kwargs
        )

    def _hiero_execute(
        self, tasks, work_template, comment, thumbnail_path, sg_task,
        primary_task, primary_publish_path, progress_cb, **kwargs
    ):
        """
        The Hiero specific secondary publish routine.
        """
        results = []
        
        # publish all tasks:
        for task in tasks:
            item = task["item"]
            output = task["output"]
            errors = []
        
            # report progress:
            progress_cb(0, "Publishing", task)
        
            # publish item here, e.g.
            #if output["name"] == "foo":
            #    ...
            #else:
            # don't know how to publish this output types!
            errors.append("Don't know how to publish this item!")   

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
             
            progress_cb(100)
             
        return results
            
    def _nuke_execute(
        self, tasks, work_template, comment, thumbnail_path, sg_task,
        primary_task, primary_publish_path, progress_cb, **kwargs
    ):
        """
        The Nuke specific secondary publish routine.
        """
        results = []

        # it's important that tasks for render output are processed
        # before tasks for quicktime output, so let's group the
        # task list by output.  This can be controlled through the
        # configuration but we shouldn't rely on that being set up 
        # correctly!
        output_order = ["render", "quicktime"]
        tasks_by_output = {}
        for task in tasks:
            output_name = task["output"]["name"]
            tasks_by_output.setdefault(output_name, list()).append(task)
            if output_name not in output_order:
                output_order.append(output_name)

        # make sure we have any apps required by the publish process:
        if "render" in tasks_by_output or "quicktime" in tasks_by_output:
            # we will need the write node app if we have any render outputs to validate
            if not self.__write_node_app:
                raise TankError("Unable to publish Shotgun Write Nodes without the tk-nuke-writenode app!")

        if "quicktime" in tasks_by_output:
            # If we have the tk-multi-reviewsubmission app we can create versions
            if not self.__review_submission_app:
                raise TankError("Unable to publish Review Versions without the tk-multi-reviewsubmission app!")

                
        # Keep of track of what has been published in shotgun
        # this is needed as input into the review creation code...
        render_publishes = {}

        # process outputs in order:
        for output_name in output_order:
            
            # process each task for this output:
            for task in tasks_by_output.get(output_name, []):
            
                # keep track of our errors for this task
                errors = []
    
                # report progress:
                progress_cb(0.0, "Publishing", task)
            
                if output_name == "render":
                    # Publish the rendered output for a Shotgun Write Node

                    # each publish task is connected to a nuke write node
                    # this value was populated via the scan scene hook
                    write_node = task["item"].get("other_params", dict()).get("node")
                    if not write_node:
                        raise TankError("Could not determine nuke write node for item '%s'!" % str(task))
        
                    # publish write-node rendered sequence                
                    try:
                        (sg_publish, thumbnail_path) = self._publish_write_node_render(task, 
                                                                                       write_node, 
                                                                                       primary_publish_path, 
                                                                                       sg_task, 
                                                                                       comment, 
                                                                                       progress_cb)
                        
                        # keep track of our publish data so that we can pick it up later in review
                        render_publishes[ write_node.name() ] = (sg_publish, thumbnail_path)
                    except Exception, e:
                        errors.append("Publish failed - %s" % e)
    
                elif output_name == "quicktime":
                    # Publish the reviewable quicktime movie for a Shotgun Write Node
    
                    # each publish task is connected to a nuke write node
                    # this value was populated via the scan scene hook
                    write_node = task["item"].get("other_params", dict()).get("node")
                    if not write_node:
                        raise TankError("Could not determine nuke write node for item '%s'!" % str(task))
        
                    # Submit published sequence to Screening Room
                    try:
                        # pick up sg data from the render dict we are maintianing
                        # note: we assume that the rendering tasks always happen
                        # before the review tasks inside the publish... 
                        (sg_publish, thumbnail_path) = render_publishes[ write_node.name() ]
                        
                        self._send_to_screening_room (
                            write_node,
                            sg_publish,
                            sg_task,
                            comment,
                            thumbnail_path,
                            progress_cb
                        )

                    except Exception, e:
                        errors.append("Submit to Screening Room failed - %s" % e)
                        
                else:
                    # unhandled output type!
                    errors.append("Don't know how to publish this item!")
    
                # if there is anything to report then add to result
                if len(errors) > 0:
                    # add result:
                    results.append({"task":task, "errors":errors})
    
                # task is finished
                progress_cb(100)            
        
        return results


    def _send_to_screening_room(self, write_node, sg_publish, sg_task, comment, thumbnail_path, progress_cb):
        """
        Take a write node's published files and run them through the review_submission app 
        to get a movie and Shotgun Version.

        :param write_node:      The Shotgun Write node to submit a review version for
        :param sg_publish:      The Shotgun publish entity dictionary to link the version with
        :param sg_task:         The Shotgun task entity dictionary for the publish
        :param comment:         The publish comment
        :param thumbnail_path:  The path to a thumbnail for the publish
        :param progress_cb:     A callback to use to report any progress
        """
        render_path = self.__write_node_app.get_node_render_path(write_node)
        render_template = self.__write_node_app.get_node_render_template(write_node)
        publish_template = self.__write_node_app.get_node_publish_template(write_node)                        
        render_path_fields = render_template.get_fields(render_path)

        if hasattr(self.__review_submission_app, "render_and_submit_version"):
            # this is a recent version of the review submission app that contains
            # the new method that also accepts a colorspace argument.
            colorspace = self._get_node_colorspace(write_node)
            self.__review_submission_app.render_and_submit_version(
                publish_template,
                render_path_fields,
                int(nuke.root()["first_frame"].value()),
                int(nuke.root()["last_frame"].value()),
                [sg_publish],
                sg_task,
                comment,
                thumbnail_path,
                progress_cb,
                colorspace
            )
        else:
            # This is an older version of the app so fall back to the legacy
            # method - this may mean the colorspace of the rendered movie is
            # inconsistent/wrong!
            self.__review_submission_app.render_and_submit(
                publish_template,
                render_path_fields,
                int(nuke.root()["first_frame"].value()),
                int(nuke.root()["last_frame"].value()),
                [sg_publish],
                sg_task,
                comment,
                thumbnail_path,
                progress_cb
            )

    def _get_node_colorspace(self, node):
        """
        Get the colorspace for the specified nuke node

        :param node:    The nuke node to find the colorspace for
        :returns:       The string representing the colorspace for the node
        """
        cs_knob = node.knob("colorspace")
        if not cs_knob:
            return
    
        cs = cs_knob.value()
        # handle default value where cs would be something like: 'default (linear)'
        if cs.startswith("default (") and cs.endswith(")"):
            cs = cs[9:-1]
        return cs

    def _publish_write_node_render(self, task, write_node, published_script_path, sg_task, comment, progress_cb):
        """
        Publish render output for write node
        """
 
        if self.__write_node_app.is_node_render_path_locked(write_node):
            # this is a fatal error as publishing would result in inconsistent paths for the rendered files!
            raise TankError("The render path is currently locked and does not match match the current Work Area.")
 
        progress_cb(10, "Finding renders")
 
        # get info we need in order to do the publish:
        render_path = self.__write_node_app.get_node_render_path(write_node)
        render_files = self.__write_node_app.get_node_render_files(write_node)
        render_template = self.__write_node_app.get_node_render_template(write_node)
        publish_template = self.__write_node_app.get_node_publish_template(write_node)                        
        tank_type = self.__write_node_app.get_node_tank_type(write_node)
        
        # publish (copy files):
        
        progress_cb(25, "Copying files")
        
        for fi, rf in enumerate(render_files):
            
            progress_cb(25 + (50*(len(render_files)/(fi+1))))
            
            # construct the publish path:
            fields = render_template.get_fields(rf)
            fields["TankType"] = tank_type
            target_path = publish_template.apply_fields(fields)

            # copy the file
            try:
                target_folder = os.path.dirname(target_path)
                self.parent.ensure_folder_exists(target_folder)
                self.parent.copy_file(rf, target_path, task)
            except Exception, e:
                raise TankError("Failed to copy file from %s to %s - %s" % (rf, target_path, e))
            
        progress_cb(40, "Publishing to Shotgun")
            
        # use the render path to work out the publish 'file' and name:
        render_path_fields = render_template.get_fields(render_path)
        render_path_fields["TankType"] = tank_type
        publish_path = publish_template.apply_fields(render_path_fields)
            
        # construct publish name:
        publish_name = ""
        rp_name = render_path_fields.get("name")
        rp_channel = render_path_fields.get("channel")
        if not rp_name and not rp_channel:
            publish_name = "Publish"
        elif not rp_name:
            publish_name = "Channel %s" % rp_channel
        elif not rp_channel:
            publish_name = rp_name
        else:
            publish_name = "%s, Channel %s" % (rp_name, rp_channel)
        
        publish_version = render_path_fields["version"]
            
        # get/generate thumbnail:
        thumbnail_path = self.__write_node_app.generate_node_thumbnail(write_node)
            
        # register the publish:
        sg_publish = self._register_publish(publish_path, 
                                            publish_name, 
                                            sg_task, 
                                            publish_version, 
                                            tank_type,
                                            comment,
                                            thumbnail_path, 
                                            [published_script_path])
        
        return sg_publish, thumbnail_path

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
        
        # register publish;
        sg_data = tank.util.register_publish(**args)
        
        return sg_data
        






