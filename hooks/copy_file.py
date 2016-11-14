# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import tank
from tank import Hook
import shutil
import os

class CopyFile(Hook):
    """
    Hook called when a file needs to be copied
    """
    
    def execute(self, source_path, target_path, task, **kwargs):
        """
        Main hook entry point
        
        :param source_path: String
                            Source file path to copy
                        
        :param target_path: String
                            Target file path to copy to
                        
        :param task:        Dictionary
                            The publish task that this file is being copied for.  This 
                            is a dictionary containing the following entries:
                            
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
        """
        
        # create the folder if it doesn't exist
        dirname = os.path.dirname(target_path)
        if not os.path.isdir(dirname):            
            old_umask = os.umask(0)
            os.makedirs(dirname, 0777)
            os.umask(old_umask)            

        shutil.copy(source_path, target_path)