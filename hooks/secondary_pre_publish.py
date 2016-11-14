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
import pyseq

import sgtk
from sgtk import Hook
from sgtk import TankError
from tank.platform.qt import QtCore, QtGui

class PrePublishHook(Hook):
    """
    Single hook that implements pre-publish functionality
    """
    def execute(self, tasks, work_template, progress_cb, user_data, **kwargs):
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

        results = []

        try:  

            self.parent.log_debug("Starting Secondary Pre Publish")

            # validate tasks:
            for task in tasks:
                item = task["item"]
                output = task["output"]
                errors = []
                app = self.parent

                # report progress:
                progress_cb(0, "Validating", task)

                if output["name"] == "alembic_cache":
                    pass
                elif output["name"] in ['cinema_render_sequences',
                                        'cinema_render_preview_video',
                                        'after_render_sequences',
                                        'after_render_preview_video']:
                                        
                    errors.extend(self.validate_render_sequences(
                        item,
                        output,
                        work_template,
                        user_data,
                        progress_cb))

                elif output['name'] in ['aftereffects_xmlproject']:

                    errors.extend(self.validate_after_xml_project(
                        item,
                        output,
                        work_template,
                        user_data,
                        progress_cb))

                elif output['name'] in ['aftereffects_element']:

                    errors.extend(self.validate_existence_of_file(item['other_params']['item_dict']['path']))

                else:
                    errors.append("Don't know how to publish this item!")

                # if there is anything to report then add to result
                if len(errors) > 0:
                    # add result:
                    results.append({"task": task, "errors": errors})

                progress_cb(100)

            self.parent.log_debug("Returning Secondary Pre Publish: %s" % results)
        except:
            import traceback
            QtGui.QMessageBox.warning(None, "Runtime Error!", traceback.format_exc())


        return results

    def validate_after_xml_project(self, item, output, work_template, user_data, progress_cb):

        """
        """

        errors = []

        schema = '<AfterEffectsProject xmlns="http://www.adobe.com/products/aftereffects" majorVersion="1" minorVersion="0">'
        if 'http://www.adobe.com/products/aftereffects' not in str(item['other_params']['xml_tree'].getroot()):

            errors.append("The header of the project file dont match the Adobe schema (%s)" % schema)


        return errors

    def validate_existence_of_file(self, path):

        """
        """
        errors = []

        if not os.path.exists(path):

            errors.append("The file %s has no longer exists on disk" % schema)


        return errors


    def validate_render_sequences(self, item, output, work_template, user_data, progress_cb):

        """
        """

        errors = []

        sequence_files = self.parent.detect_image_sequence(item['other_params']['item_dict']['path'] % 1)
        sequences = pyseq.get_sequences(sequence_files)

        for seq in sequences:

            if len(seq.missing()) != 0:
                errors.append("Your sequence has %s missing frames, it could not be published. (%s)" % (str(len(seq.missing())), seq.missing()))


        return errors