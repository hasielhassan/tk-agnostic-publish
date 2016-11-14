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

        self.log_debug("Initializing tk-agnostic-publish")
        
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
        
        self.log_debug("Registering command for tk-agnostic-publish")
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
        self.log_debug("Destroying tk-agnostic-publish")
        
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


    def detect_image_sequence(self, filepath):

        """
        Method to retrieve a list of sequence files corresponding to the input filepath
        http://blender.stackexchange.com/questions/21092/how-to-get-all-images-for-an-image-sequence-from-python
        """

        basedir, filename = os.path.split(filepath)
        filename_noext, ext = os.path.splitext(filename)

        from string import digits
        if isinstance(filepath, bytes):
            digits = digits.encode()
        filename_nodigits = filename_noext.rstrip(digits)

        if len(filename_nodigits) == len(filename_noext):
            # input isn't from a sequence
            return []

        files = os.listdir(basedir)
        elements = [
            os.path.join(basedir, f)
            for f in files
            if f.startswith(filename_nodigits) and
               f.endswith(ext) and
               f[len(filename_nodigits):-len(ext) if ext else -1].isdigit()]

        return elements

    def _get_publish_name(self, path, template, fields=None):
        """
        Return the 'name' to be used for the file - if possible
        this will return a 'versionless' name
        """
        # first, extract the fields from the path using the template:
        fields = fields.copy() if fields else template.get_fields(path)
        '''
        if "name" in fields and fields["name"]:
            # well, that was easy!
            name = fields["name"]
        else:
        '''
        # find out if version is used in the file name:
        template_name, _ = os.path.splitext(os.path.basename(template.definition))
        version_in_name = "{version}" in template_name
        artist_in_name = '{artist}' in template_name

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

        if artist_in_name:
            artist = fields['artist']
            a_pos = name.find(artist)
            pre_a_str = name[:a_pos]
            post_a_str = name[a_pos + len(artist):]
            if (pre_a_str and post_a_str
                and pre_a_str[-1] in delims_str
                and post_a_str[0] in delims_str):
                # only want one delimiter - strip the second one:
                post_v_str = post_v_str.lstrip(delims_str)

            artistless_name = pre_a_str + post_a_str
            artistless_name = artistless_name.strip(delims_str)

            if artistless_name:
                name = artistless_name
            else:
                name = name.replace(artist, 'artist')

        return name