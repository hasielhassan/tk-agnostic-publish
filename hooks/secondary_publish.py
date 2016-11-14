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
import re
import sys
import pyseq
import shutil
import tempfile
import traceback
import subprocess

import tank
from tank import Hook
from tank import TankError
from tank.platform.qt import QtCore, QtGui

class PublishHook(Hook):
    """
    Single hook that implements publish functionality for secondary tasks
    """
    def execute(
        self, tasks, work_template, comment, thumbnail_path, sg_task, primary_task,
        primary_publish_path, progress_cb, user_data, **kwargs):
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
        results = []

        # publish all tasks:
        for task in tasks:
            publish_task = task
            item = task["item"]
            output = task["output"]
            errors = []
            app = self.parent

            # report progress:
            progress_cb(0, "Publishing", task)

            if output["name"] == "alembic_cache":
                self.__publish_alembic_cache(
                    item,
                    output,
                    work_template,
                    primary_publish_path,
                    sg_task,
                    publish_task,
                    comment,
                    thumbnail_path,
                    progress_cb,
                )
            elif output["name"] in ["cinema_render_sequences", "after_render_sequences"]:
                self.__publish_render_sequences(
                    item,
                    output,
                    work_template,
                    primary_publish_path,
                    sg_task,
                    publish_task,
                    comment,
                    thumbnail_path,
                    progress_cb,
                )
            elif output["name"] in ["cinema_render_preview_video", "after_render_preview_video"]:
                self.__publish_preview_video(
                    item,
                    output,
                    work_template,
                    primary_publish_path,
                    sg_task,
                    publish_task,
                    comment,
                    thumbnail_path,
                    progress_cb,
                )
            elif output["name"] in ["aftereffects_element"]:
                self.__publish_simple_element(
                    item,
                    output,
                    work_template,
                    primary_publish_path,
                    sg_task,
                    publish_task,
                    comment,
                    thumbnail_path,
                    progress_cb,
                )
            elif output["name"] in ["aftereffects_xmlproject"]:
                self.__publish_after_xml_project(
                    item,
                    output,
                    work_template,
                    primary_publish_path,
                    sg_task,
                    publish_task,
                    comment,
                    thumbnail_path,
                    progress_cb,
                )

            else:
                errors.append("Don't know how to publish this item!")

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task": task, "errors": errors})

            progress_cb(100)

        return results


    def __publish_simple_element(
        self, item, output, work_template, primary_publish_path, 
        sg_task, publish_task, comment, thumbnail_path, progress_cb):
        """
        Publish an Image Sequence for the scene and publish it to Shotgun.
        
        :param item:                    The item to publish
        :param output:                  The output definition to publish with
        :param work_template:           The work template for the current scene
        :param primary_publish_path:    The path to the primary published file
        :param sg_task:                 The Shotgun task we are publishing for
        :param comment:                 The publish comment/description
        :param thumbnail_path:          The path to the publish thumbnail
        :param progress_cb:             A callback that can be used to report progress
        """
        # determine the publish info to use
        #
        progress_cb(10, "Determining publish details")

        # get the current scene path and extract fields from it
        # using the work template:
        element_path = item['other_params']['item_dict']['path']
        tank_type = output["tank_type"]
        publish_template = output['publish_template']
        publish_path = item['other_params']['publish_path']    

        # ensure the publish folder exists:
        publish_folder = os.path.dirname(publish_path)
        self.parent.ensure_folder_exists(publish_folder)

        # determine the publish name:
        publish_name = self.parent._get_publish_name(publish_path, publish_template)

        progress_cb(30, "Copying file to PublishArea")

        self.parent.copy_file(element_path, publish_path, publish_task)

        # register the publish:
        publish_version = item['other_params']['fields']['version']
        progress_cb(90, "Registering the publish")        
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": comment,
            "path": publish_path,
            "name": publish_name,
            "version_number": publish_version,
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "dependency_paths": [primary_publish_path],
            "published_file_type":tank_type
        }
        tank.util.register_publish(**args)

    def __publish_after_xml_project(
        self, item, output, work_template, primary_publish_path, 
        sg_task, publish_task, comment, thumbnail_path, progress_cb):
        """
        Publish an Image Sequence for the scene and publish it to Shotgun.
        
        :param item:                    The item to publish
        :param output:                  The output definition to publish with
        :param work_template:           The work template for the current scene
        :param primary_publish_path:    The path to the primary published file
        :param sg_task:                 The Shotgun task we are publishing for
        :param comment:                 The publish comment/description
        :param thumbnail_path:          The path to the publish thumbnail
        :param progress_cb:             A callback that can be used to report progress
        """
        # determine the publish info to use
        #
        progress_cb(10, "Determining publish details")

        # get the current scene path and extract fields from it
        # using the work template:
        tank_type = output["tank_type"]
        publish_template = output['publish_template']
        publish_path = item['other_params']['publish_path']    

        # ensure the publish folder exists:
        publish_folder = os.path.dirname(publish_path)
        self.parent.ensure_folder_exists(publish_folder)

        # determine the publish name:
        publish_name = self.parent._get_publish_name(publish_path, publish_template)

        progress_cb(30, "Copying file to PublishArea")

        
        #replace all the reference paths with the publish ones
        after_tree = item['other_params']['xml_tree']
        references_dict = item['other_params']['references_dict']
        self.after_recurse_update_fileReference(after_tree.getroot(), references_dict)

        #save modified xml tree
        after_tree.write(publish_path)


        # register the publish:
        publish_version = item['other_params']['fields']['version']
        progress_cb(90, "Registering the publish")        
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": comment,
            "path": publish_path,
            "name": publish_name,
            "version_number": publish_version,
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "dependency_paths": [primary_publish_path],
            "published_file_type":tank_type
        }
        tank.util.register_publish(**args)


    def __publish_render_sequences(
        self, item, output, work_template, primary_publish_path, 
        sg_task, publish_task, comment, thumbnail_path, progress_cb):
        """
        Publish an Image Sequence for the scene and publish it to Shotgun.
        
        :param item:                    The item to publish
        :param output:                  The output definition to publish with
        :param work_template:           The work template for the current scene
        :param primary_publish_path:    The path to the primary published file
        :param sg_task:                 The Shotgun task we are publishing for
        :param comment:                 The publish comment/description
        :param thumbnail_path:          The path to the publish thumbnail
        :param progress_cb:             A callback that can be used to report progress
        """
        # determine the publish info to use
        #
        progress_cb(10, "Determining publish details")

        # get the current scene path and extract fields from it
        # using the work template:
        sequence_path = item['other_params']['item_dict']['path']
        sequence_files = self.parent.detect_image_sequence(sequence_path % 1)
        tank_type = output["tank_type"]
        
        work_template = item['other_params']['work_template']
        publish_template = output['publish_template']
        publish_path = item['other_params']['publish_path']         
        
        # ensure the publish folder exists:
        publish_folder = os.path.dirname(publish_path)
        self.parent.ensure_folder_exists(publish_folder)

        # determine the publish name:
        publish_name = self.parent._get_publish_name(publish_path, publish_template)
        base_message = "Copying sequence to PublishArea"
        progress_cb(30, base_message)
        sequence_elements = sorted(self.parent.detect_image_sequence(sequence_path % 1))

        current_progress = 30
        item_progress = 60.0 / len(sequence_elements)
        for work_element_path in sequence_elements:

            current_progress += item_progress
            fields = work_template.get_fields(work_element_path)
            padding = fields['SEQ']

            progress_cb(current_progress, "%s - %s" % (base_message, padding))

            publish_element_path = publish_path % padding

            self.parent.copy_file(work_element_path, publish_element_path, publish_task)


        # register the publish:
        publish_version = item['other_params']['fields']['version']
        progress_cb(90, "Registering the publish")        
        args = {
            "tk": self.parent.tank,
            "context": self.parent.context,
            "comment": comment,
            "path": publish_path,
            "name": publish_name,
            "version_number": publish_version,
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "dependency_paths": [primary_publish_path],
            "published_file_type":tank_type
        }
        tank.util.register_publish(**args)


    def __publish_preview_video(
        self, item, output, work_template, primary_publish_path, 
        sg_task, publish_task, comment, thumbnail_path, progress_cb):
        """
        Publish an Image Sequence for the scene and publish it to Shotgun.
        
        :param item:                    The item to publish
        :param output:                  The output definition to publish with
        :param work_template:           The work template for the current scene
        :param primary_publish_path:    The path to the primary published file
        :param sg_task:                 The Shotgun task we are publishing for
        :param comment:                 The publish comment/description
        :param thumbnail_path:          The path to the publish thumbnail
        :param progress_cb:             A callback that can be used to report progress
        """
        # determine the publish info to use
        #
        progress_cb(5, "Determining publish details")

        try:
            sequence_path = item['other_params']['item_dict']['path']
            sequence_elements = sorted(self.parent.detect_image_sequence(sequence_path % 1))
            sequence = pyseq.Sequence(sequence_elements)

            frames_length = sequence.length()
            image_start_number = sequence.start()
            image_end_number = sequence.end()


            progress_cb(15, "Preparing to Create Video") 

            publish_template = output['publish_template']
            fields = item['other_params']['fields']
            publish_version = fields["version"]
            tank_type = output["tank_type"]

            publish_path = publish_template.apply_fields(fields)
            publish_folder = os.path.dirname(publish_path)
            publish_name = self.parent._get_publish_name(publish_path, publish_template)
            self.parent.ensure_folder_exists(publish_folder)

            progress_cb(30, "Creating Scene Video")

            temporal_path = 'C:/tmp'
            if not os.path.exists (temporal_path):
                os.makedirs (temporal_path)
            temporal_file = os.path.join(temporal_path, 'temporal_video.mov')

            input_frame_rate = 24

            progress_cb(40, "Transcoding renders to sRGB")
            temp_path = self.set_temporal_transcoding(sequence_path).replace('.exr', '.jpg')
            self.parent.log_debug("Temporal transcoding path: %s" % temp_path)

            progress_cb(60, "Transcoding renders into video")
            convert_cmd = ['ffmpeg',
                         '-r',
                         str(input_frame_rate),
                         '-i',
                         temp_path,
                         '-vcodec',
                         'libx264',
                         '-pix_fmt',
                         'yuv420p',
                         '-preset',
                         'slow',
                         '-crf',
                         '5',
                         '-vf',
                         'scale=trunc(iw/2)*2:trunc(ih/2)*2,setsar=1/1',
                         '-y',
                         '-r',
                         '24',
                         temporal_file]


            self.parent.log_debug ("convert_cmd created as: %s" % convert_cmd)
            preview_video = subprocess.Popen(convert_cmd, startupinfo = subprocess.STARTUPINFO(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            self.parent.log_debug ("doing playblast command")
            stdout, stderr = preview_video.communicate()
            self.parent.log_debug ("ffmpeg thingy done")

            if preview_video.returncode != 0:
                raise Exception("Failed to convert playblast to video: %s" % (str(stderr) + '\n' + str(stdout) + '\n' + str(convert_cmd)))

            shutil.move(temporal_file, publish_path)


            # register the publish:
            progress_cb(80, "Registering the publish")        
            args = {
                "tk": self.parent.tank,
                "context": self.parent.context,
                "comment": comment,
                "path": publish_path,
                "name": publish_name,
                "version_number": publish_version,
                "thumbnail_path": thumbnail_path,
                "task": sg_task,
                "dependency_paths": [primary_publish_path],
                "published_file_type":tank_type
            }
            sg_publishes = tank.util.register_publish(**args)


            #creating SHotgun Version
            progress_cb(90, "Creating Shotgun Version")
            sg_version = self.submit_version(sequence_path, 
                                              publish_path,
                                              [sg_publishes], 
                                              sg_task, 
                                              comment, 
                                              True,
                                              image_start_number, 
                                              image_end_number)

            # Upload in a new thread and make our own event loop to wait for the
            # thread to finish.
            progress_cb(95, "Uploading to Shotgun")
            event_loop = QtCore.QEventLoop()
            thread = UploaderThread(self.parent, sg_version, publish_path, thumbnail_path, True)
            thread.finished.connect(event_loop.quit)
            thread.start()
            event_loop.exec_()

            try:
                if os.path.exists(temp_path):
                    shutil.rmtree(temp_path)
            except:
                pass

            progress_cb(100, "Done") 
        except:
            error = traceback.format_exc()
            self.parent.log_error (error)
            raise TankError (error)



    def set_temporal_transcoding(self, preview_temp):

        """
        Method to transcode the exr sequence into a sRGB jpg one
        """

        tmp_transcode_dir = tempfile.gettempdir()

        filename, ext = os.path.splitext(os.path.basename(preview_temp))
        filename, padding = os.path.splitext(filename)
        folderfiles = os.listdir(os.path.dirname(preview_temp))

        sequence_files = []
        for file in sorted(folderfiles):
            if file.startswith(filename) and file.endswith(ext):
                sequence_files.append(file)

        if not os.path.exists(tmp_transcode_dir):
            os.makedirs(tmp_transcode_dir)

        current = 1
        for i in sequence_files:
            from_source = os.path.dirname(preview_temp) + os.path.sep + i
            to_dest = tmp_transcode_dir + (filename + padding + ".jpg") % current

            convert_cmd = [self.get_imagemagick(),
                           from_source,
                           '-set',
                           '-colorspace',
                           'RGB',
                           '-colorspace',
                           'sRGB',
                           to_dest]

            CREATE_NO_WINDOW = 0x08000000
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            linear_to_srgb = subprocess.Popen(convert_cmd,
                                              startupinfo = startupinfo,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              stdin=subprocess.PIPE,
                                              creationflags=CREATE_NO_WINDOW)
            stdout, stderr = linear_to_srgb.communicate()

            if linear_to_srgb.returncode != 0:
                raise Exception(str(stderr) + '\n' + str(stdout))

            current += 1

        to_dest_2 = tmp_transcode_dir + (filename + padding + '.jpg') % current
        shutil.copy(to_dest, to_dest_2)

        temp_transcode_path = tmp_transcode_dir + (filename + padding + ext)

        return temp_transcode_path

    def get_imagemagick(self):

        if os.environ.get('IMAGEMAGICK'):

            path = os.path.join(os.environ.get('IMAGEMAGICK'), 'convert')

        else:
            if sys.platform == 'win32':
                path = 'C:\\ImageMagick\\convert'
            else:
                path = '/etc/imagemagick/bin/convert'

        if sys.platform == 'win32':

            path += ".exe"

        if not os.path.exists(path):

            raise Exception("Cant found image ImageMagick convert executable in path: %s" % path)

        return path

    def after_recurse_update_fileReference(self, element, references_dict):
        """
        Method to collect all fileReference items in the xml project
        """
        for child in element.getchildren():

            if 'fileReference' in child.tag:
                reference = { key: value for key, value in child.attrib.iteritems()}
                if reference['fullpath'] in references_dict:
                    child.attrib['fullpath'] = references_dict[reference['fullpath']]

            self.after_recurse_update_fileReference(child, references_dict)



    def submit_version(self, path_to_frames, path_to_movie, sg_publishes,
                        sg_task, comment, store_on_disk, first_frame, last_frame, override_entity=False):
        """
        Create a version in Shotgun for this path and linked to this publish.
        """
        
        # get current shotgun user
        current_user = tank.util.get_current_user(self.parent.tank)
        
        # create a name for the version based on the file name
        # grab the file name, strip off extension
        name = os.path.splitext(os.path.basename(path_to_movie))[0]
        # do some replacements
        name = name.replace("_", " ")
        # and capitalize
        name = name.capitalize()

        LinkFolder = {'local_path': os.path.dirname(path_to_frames) + os.sep,
                        'content_type': None,
                        'link_type': 'local',
                        'name': name}

        LinkFile = {'local_path': path_to_movie,
                        'content_type': None,
                        'link_type': 'local',
                        'name': name}
        
        if override_entity != False:
            entity = override_entity
        else:
            entity = self.parent.context.entity

        # Create the version in Shotgun
        data = {
            "code": name,
            "entity": entity,
            "sg_task": sg_task,
            "sg_first_frame": first_frame,
            "sg_last_frame": last_frame,
            "frame_count": (last_frame-first_frame+1),
            "frame_range": "%s-%s" % (first_frame, last_frame),
            "sg_frames_have_slate": False,
            "published_files": sg_publishes,
            "created_by": current_user,
            "description": comment,
            "sg_path_to_frames": path_to_frames,
            "sg_movie_has_slate": True,
            "project": self.parent.context.project,
            "user": current_user
        }

        if store_on_disk:
            data["sg_path_to_movie"] = path_to_movie

        sg_version = self.parent.tank.shotgun.create("Version", data)
        self.parent.log_debug("Created version in shotgun: %s" % str(data))
        return sg_version



class UploaderThread(QtCore.QThread):
    """
    Simple worker thread that encapsulates uploading to shotgun.
    Broken out of the main loop so that the UI can remain responsive
    even though an upload is happening
    """
    def __init__(self, app, version, path_to_movie, thumbnail_path, upload_to_shotgun):
        QtCore.QThread.__init__(self)
        self._app = app
        self._version = version
        self._path_to_movie = path_to_movie
        self._thumbnail_path = thumbnail_path
        self._upload_to_shotgun = upload_to_shotgun
        self._errors = []

    def get_errors(self):
        """
        can be called after execution to retrieve a list of errors
        """
        return self._errors

    def run(self):
        """
        Thread loop
        """
        upload_error = False

        if self._upload_to_shotgun:
            try:
                self._app.tank.shotgun.upload("Version", self._version["id"], self._path_to_movie, "sg_uploaded_movie")
            except Exception, e:
                self._errors.append("Movie upload to Shotgun failed: %s" % e)
                upload_error = True

        if not self._upload_to_shotgun or upload_error:
            try:
                self._app.tank.shotgun.upload_thumbnail("Version", self._version["id"], self._thumbnail_path)
            except Exception, e:
                self._errors.append("Thumbnail upload to Shotgun failed: %s" % e)