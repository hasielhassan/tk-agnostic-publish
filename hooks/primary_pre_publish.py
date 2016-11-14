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
        
        # depending on engine:
        if engine_name == "tk-maya":
            return self._do_maya_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-motionbuilder":
            return self._do_motionbuilder_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-hiero":
            return self._do_hiero_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-nuke":
            return self._do_nuke_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-3dsmax":
            return self._do_3dsmax_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-3dsmaxplus":
            return self._do_3dsmaxplus_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-houdini":
            return self._do_houdini_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-softimage":
            return self._do_softimage_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-photoshop":
            return self._do_photoshop_pre_publish(task, work_template, progress_cb, user_data)
        elif engine_name == "tk-mari":
            return self._do_mari_pre_publish(task, work_template, progress_cb, user_data)
        else:
            raise TankError("Unable to perform pre-publish for unhandled engine %s" % engine_name)
        
    def _do_maya_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Maya primary pre-publish/scene validation

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
        import maya.cmds as cmds
        
        progress_cb(0.0, "Validating current scene", task)
        
        # get the current scene file:
        scene_file = cmds.file(query=True, sn=True)
        if scene_file:
            scene_file = os.path.abspath(scene_file)
            
        # validate it:
        scene_errors = self._validate_work_file(scene_file, work_template, task["output"], progress_cb)
        
        progress_cb(100)
          
        return scene_errors
        
    def _do_motionbuilder_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Motion Builder primary pre-publish/scene validation

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
        from pyfbsdk import FBApplication

        mb_app = FBApplication()

        progress_cb(0, "Validating current script", task)

        # get the current script file path:
        script_file = mb_app.FBXFileName
        if script_file:
            script_file = os.path.abspath(script_file)

        # validate it
        script_errors = self._validate_work_file(script_file, work_template, task["output"], progress_cb)

        progress_cb(100)

        return script_errors

    def _do_3dsmax_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do 3ds Max primary pre-publish/scene validation

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
        from Py3dsMax import mxs
        
        progress_cb(0.0, "Validating current scene", task)
        
        # get scene path
        scene_path = os.path.abspath(os.path.join(mxs.maxFilePath, mxs.maxFileName))
            
        # validate it:
        scene_errors = self._validate_work_file(scene_path, work_template, task["output"], progress_cb)
        
        progress_cb(100)
          
        return scene_errors
        
    def _do_3dsmaxplus_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do 3ds Max primary pre-publish/scene validation

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
        import MaxPlus
        
        progress_cb(0.0, "Validating current scene", task)
        
        # get scene path
        scene_path = MaxPlus.FileManager.GetFileNameAndPath()
            
        # validate it:
        scene_errors = self._validate_work_file(scene_path, work_template, task["output"], progress_cb)
        
        progress_cb(100)
          
        return scene_errors

    def _do_nuke_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Nuke primary pre-publish/scene validation

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
        # If we're in Hiero or Nuke Studio, then we call through to those.
        engine = self.parent.engine

        if hasattr(engine, "hiero_enabled") and engine.hiero_enabled:
            return self._do_hiero_pre_publish(task, work_template, progress_cb, user_data)
        elif hasattr(engine, "studio_enabled") and engine.studio_enabled:
            return self._do_nukestudio_pre_publish(task, work_template, progress_cb, user_data)

        import nuke
        
        progress_cb(0, "Validating current script", task)
        
        # get the current script file path:
        script_file = nuke.root().name().replace("/", os.path.sep)
        if script_file:
            script_file = os.path.abspath(script_file)
            
        # validate it
        script_errors = self._validate_work_file(script_file, work_template, task["output"], progress_cb)
        
        progress_cb(100)
        
        return script_errors

    def _do_nukestudio_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Nuke Studio primary pre-publish/scene validation

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
        # Out of the box, we treat Nuke Studio the same as we do Hiero.
        return self._do_hiero_pre_publish(task, work_template, progress_cb, user_data)
        
    def _do_hiero_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Hiero primary pre-publish/scene validation

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
        import hiero.core
        
        progress_cb(0.0, "Validating current Project", task)

        # first find which the current project is. Hiero is a multi project 
        # environment so we can ask the engine which project was clicked in order
        # to launch this publish.        
        selection = self.parent.engine.get_menu_selection()
        
        # these values should in theory already be validated, but just in case...
        if len(selection) != 1:
            raise TankError("Please select a single Project!")
        if not isinstance(selection[0] , hiero.core.Bin):
            raise TankError("Please select a Hiero Project!")
        project = selection[0].project()
        if project is None:
            # apparently bins can be without projects (child bins I think)
            raise TankError("Please select a Hiero Project!")

        # get the current scene file:
        scene_path = os.path.abspath(project.path().replace("/", os.path.sep))

        # validate it:
        project_errors = self._validate_work_file(scene_path, work_template, task["output"], progress_cb)

        progress_cb(100)
        
        return project_errors
        
    def _do_houdini_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Houdini primary pre-publish/scene validation

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
        import hou

        progress_cb(0, "Validating current script", task)

        # get the current script file path:
        script_file = hou.hipFile.name()
        if script_file:
            script_file = os.path.abspath(script_file)

        # validate it
        script_errors = self._validate_work_file(script_file, work_template, task["output"], progress_cb)

        progress_cb(100)

        return script_errors

    def _do_softimage_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Softimage primary pre-publish/scene validation

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
        import win32com
        from win32com.client import Dispatch, constants
        from pywintypes import com_error
        Application = Dispatch("XSI.Application").Application

        progress_cb(0, "Validating current scene", task)

        # query the current scene 'name' from the application:
        scene_filepath = Application.ActiveProject.ActiveScene.filename.value
                    
        # There doesn't seem to be an easy way to determin if the current scene 
        # is 'new'.  However, if the file name is "Untitled.scn" and the scene 
        # name is "Scene" rather than "Untitled", then we can be reasonably sure 
        # that we haven't opened a file called Untitled.scn
        scene_name = Application.ActiveProject.ActiveScene.Name
        if scene_name == "Scene" and os.path.basename(scene_filepath) == "Untitled.scn":
            scene_filepath = ""
        else:
            scene_filepath = os.path.abspath(scene_filepath)

        # validate it
        scene_errors = self._validate_work_file(scene_filepath, work_template, task["output"], progress_cb)

        progress_cb(100)

        return scene_errors

    def _do_photoshop_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Do Photoshop primary pre-publish/scene validation

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
        import photoshop
        
        progress_cb(0.0, "Validating current scene", task)
        
        # get the current scene file:
        doc = photoshop.app.activeDocument
        if doc is None:
            raise TankError("There is no currently active document!")
        
        scene_file = doc.fullName.nativePath
            
        # validate it:
        scene_errors = self._validate_work_file(scene_file, work_template, task["output"], progress_cb)
        
        progress_cb(100)
          
        return scene_errors

    def _do_mari_pre_publish(self, task, work_template, progress_cb, user_data):
        """
        Perform any pre-publish for the primary task in Mari.
        
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
        # currently there is no primary publish for Mari so just return
        return []


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
        
