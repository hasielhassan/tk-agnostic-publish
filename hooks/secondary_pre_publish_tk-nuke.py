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
import nuke

import tank
from tank import Hook
from tank import TankError

class PrePublishHook(Hook):
    """
    Single hook that implements pre-publish functionality
    """
    def execute(self, *args, **kwargs):
        """
        Main hook entry point
        :param tasks:           List of tasks to be pre-published.  Each task is be a 
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
                        
        :returns:               A list of any tasks that were found which have problems that
                                need to be reported in the UI.  Each item in the list should
                                be a dictionary containing the following keys:
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

    def _studio_execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        The Nuke Studio specific routine for secondary pre-publish.
        """
        # We treat Nuke Studio the same as Hiero, so call through.
        return self._hiero_execute(tasks, work_template, progress_cb, **kwargs)

    def _hiero_execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        The Hiero specific routine for secondary pre-publish.
        """
        results = []
        progress_cb(100)
        return results

    def _nuke_execute(self, tasks, work_template, progress_cb, **kwargs):
        """
        The Nuke specific routine for secondary pre-publish.
        """
        results = []

        # we will need the write node app if we have any render outputs to validate
        write_node_app = self.parent.engine.apps.get("tk-nuke-writenode")
        
        # validate tasks:
        for task in tasks:
            item = task["item"]
            output = task["output"]
            errors = []
        
            # report progress:
            progress_cb(0.0, "Validating", task)
        
            # depending on output type, do some specific validation:
            if output["name"] == "render":
                # validate that the write node has rendered images to publish:
                # ...
                if not write_node_app:
                    errors.append("Unable to validate write node '%s' without tk-nuke-writenode app!" % item["name"])
                else:
                    # get write node:
                    write_node = item.get("other_params", dict()).get("node")
                    if not write_node:
                        errors.append("Could not find nuke node for item '%s'!" % item["name"])
                    else:
                        # do pre-publish:              
                        errors = self._nuke_pre_publish_write_node_render(write_node, write_node_app, progress_cb)
            
            elif output["name"] == "quicktime":
                # Make sure a 'Publish Renders' task is checked.
                if not self._get_render_task_for_task(tasks, task):
                    raise TankError("If you have the 'Send to Screening Room' box ticked, you "
                                    "must also have the 'Publish Renders' box ticked!")

                # the render task will always render full-res frames when publishing. If we're
                # in proxy mode in Nuke, that task will fail since there will be no full-res 
                # frames rendered. The exceptions are if there is no proxy_render_template set 
                # in the tk-nuke-writenode app, then the write node app falls back on the
                # full-res template. Or if they rendered in full res and then switched to 
                # proxy mode later. In this case, this is likely user error, so we catch it.
                root_node = nuke.root()
                proxy_mode_on = root_node['proxy'].value()
                if proxy_mode_on:
                    raise TankError("You cannot publish to Screening Room while Nuke is in proxy "
                                    "mode. Please toggle proxy mode OFF and try again.")
            
            else:
                # don't know how to publish other output types!
                errors.append("Don't know how to publish this item!")      

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
            
            progress_cb(100)
            
        return results
        
    def _get_render_task_for_task(self, tasks, ref):
        """
        Given a list of tasks, find the one render task who's Nuke node name is
        the same as the Nuke node name in the reference task.
        """
        for task in tasks:
            if task["output"]["name"] != "render":
                continue

            task_node = task["item"].get("other_params", dict()).get("node")
            ref_node = ref["item"].get("other_params", dict()).get("node")
            if not task_node or not ref_node:
                continue

            if task_node.name() == ref_node.name():
                return task

        return None

    def _nuke_pre_publish_write_node_render(self, write_node, write_node_app, progress_cb):
        """
        Pre-publish render output for write node
        """
        errors = []
        try:
            # check to see if the write node path is currently locked:
            if write_node_app.is_node_render_path_locked(write_node):
                # renders for the write node can't be published - trying to publish 
                # will result in an error in the publish hook!
                errors.append("The render path is currently locked and does not match match the current Work Area.")
            
            progress_cb(10.0, "Finding rendered files")
            
            # get list of render files:
            render_files = write_node_app.get_node_render_files(write_node)
            if len(render_files) == 0:
                is_valid = False
                errors.append("No render files exist to be published!")
            else:
                # ensure that published files don't already exist
        
                # need the render template, publish template and tank type which are all 
                # defined per node (profile) in the tk-nuke-writenode app
                render_template = write_node_app.get_node_render_template(write_node)
                publish_template = write_node_app.get_node_publish_template(write_node)                        
                tank_type = write_node_app.get_node_tank_type(write_node)
        
                progress_cb(25.0, "Checking for existing files")
                
                # check files:
                existing_files = []
                for fi, rf in enumerate(render_files):
                    
                    progress_cb(25 + (75*(len(render_files)/(fi+1))))
                    
                    # construct the publish path:
                    fields = render_template.get_fields(rf)
                    fields["TankType"] = tank_type
                    target_path = publish_template.apply_fields(fields)
                
                    if os.path.exists(target_path):
                        existing_files.append(target_path)
                        
                if existing_files:
                    # one or more published files already exist!
                    msg = "Published render file '%s'" % existing_files[0]
                    if len(existing_files) > 1:
                        msg += " (+%d others)" % (len(existing_files)-1)
                    msg += " already exists!"
                    errors.append(msg)
        except Exception, e:
            errors.append("Unhandled exception: %s" % e)

        return errors
    
    
    