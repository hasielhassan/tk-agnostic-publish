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
import mari

import sgtk
from sgtk import Hook
from sgtk import TankError

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
        self.__cached_publishes = None
        
        results = []
        
        # publish all tasks:
        for task in tasks:
            item = task["item"]
            output = task["output"]
            errors = []
        
            # report progress:
            progress_cb(0, "Publishing", task)
        
            # publish channel and layer outputs:
            if output["name"] in ["channel", "layer"]:
                # publish images for a layer or channel
                try:
                    self._publish_textures(item, output, sg_task, comment, thumbnail_path, progress_cb)
                except TankError, e:
                    errors.append("Publish failed - %s" % e)
            else:
                # don't know how to publish this output types!
                errors.append("Don't know how to publish this item!")    

            # if there is anything to report then add to result
            if len(errors) > 0:
                # add result:
                results.append({"task":task, "errors":errors})
             
            progress_cb(100)
             
        return results
    
    def _publish_textures(self, item, output, sg_task, comment, thumbnail_path, progress_cb):
        """
        Publish textures for Mari geometry
        
        :param item:            The item to publish
        :param output:          The output definition for the item
        :param sg_task:         The Shotgun task the publish should be associated with
        :param comment:         The comment/description for the publish
        :param thumbnail_path:  Path to the thumbnail to use for the publish
        :param progress_cb:     Callback to report all progress through
        """
        mari_engine = self.parent.engine
        
        # extract the geo, channel & layer from the other params - these
        # were determined in the scan scene hook.
        params = item.get("other_params")
        geo_name = params["geo"]
        channel_name = params["channel"]
        layer_name = params.get("layer")
        
        progress_cb(10, "Finding geometry details")
        
        # find the channel & geo to publish:
        geo = mari.geo.find(geo_name)
        if not geo:
            raise TankError("Failed to find geometry '%s'!" % geo_name)
        
        channel = geo.findChannel(channel_name)
        if not channel:
            raise TankError("Failed to find channel '%s' on '%s'!" % (channel_name, geo_name))
        publish_name = "%s, %s" % (geo_name, channel_name)
        
        layer = None
        if layer_name:
            layer = channel.findLayer(layer_name)
            if not layer:
                raise TankError("Failed to find layer '%s' in channel '%s' on '%s'!" % (layer_name, channel_name, geo_name))
            publish_name = "%s, %s - %s" % (geo_name, channel_name, layer_name)

        # build the publish output path:
        progress_cb(20, "Building publish path")
        publish_template = output["publish_template"]
        fields = {}
        
        # use these fields to generate the publish path:
        publish_path = None
        try:        
        
            # 1. Get fields from geo publish path if possible
            geo_version = geo.currentVersion()
            geo_version_info = mari_engine.get_shotgun_info(geo_version)
            geo_publish_path = geo_version_info.get("path")
            if geo_publish_path:
                try:
                    geo_publish_template = self.parent.sgtk.template_from_path(geo_publish_path)
                    fields = geo_publish_template.get_fields(geo_publish_path)
                except TankError:
                    # ok, so don't worry about the fields from the geometry publish!
                    pass
            
            # 2. Get fields from the current context
            ctx_fields = self.parent.context.as_template_fields(publish_template)
            fields.update(ctx_fields)
            
            # 3. Use the name from the geo - this will be the name from the geo publish but
            # may also incorporate the mesh name if multiple objects were loaded from the same
            # publish
            fields["name"] = geo_name
            
            # 4. Add in channel and layer names:
            fields["channel"] = channel_name
            if layer:
                fields["layer"] = layer_name
            
            # 5. Find next version to use - note that version may be different across channels and/or layers        
            progress_cb(30, "Finding next publish version to use")
            existing_publishes = self.__find_publishes(self.parent.context, publish_name, output["tank_type"])
            fields["version"] = max([p["version_number"] for p in existing_publishes] or [0]) + 1        

            publish_path = publish_template.apply_fields(fields)
        except TankError, e:
            raise TankError("Failed to build a publish path: %s" % e)
        
        # and also generate the Mari output path using the Mari tokens for UDIM, channel & layer:
        output_path = None
        try:
            fields["UDIM"] = "$UDIM"
            output_path = publish_template.apply_fields(fields)
        except TankError, e:
            raise TankError("Failed to build the Mari output path: %s" % e)
        
        # ensure the publish folder exists:
        publish_folder = os.path.dirname(publish_path)
        self.parent.ensure_folder_exists(publish_folder)
        
        # publish the layer:
        if layer:
            # publish a specific layer:
            progress_cb(50, "Exporting layer")
            layer.exportImages(output_path)
        else:
            # publish the entire channel, flattened
            progress_cb(50, "Exporting channel")
            layers = channel.layerList()
            if len(layers) == 1:
                # only one layer so just publish it:
                # Note - this works around an issue that was reported (#27945) where flattening a channel
                # with only a single layer would cause Mari to crash - this bug was not reproducible by
                # us but happened 100% for the client!
                layer = layers[0]
                layer.exportImages(output_path)
            elif len(layers) > 1:
                # flatten layers in the channel and publish the flattened layer:
                # remember the current channel:
                current_channel = geo.currentChannel()
                # duplicate the channel so we don't operate on the original:
                duplicate_channel = geo.createDuplicateChannel(channel)
                try:
                    # flatten it into a single layer:
                    flattened_layer = duplicate_channel.flatten()
                    # export the images for it:
                    flattened_layer.exportImages(output_path)
                finally:
                    # set the current channel back - not doing this will result in Mari crashing
                    # when the duplicated channel is removed!
                    geo.setCurrentChannel(current_channel)
                    # remove the duplicate channel, destroying the channel and the flattened layer:
                    geo.removeChannel(duplicate_channel, geo.DESTROY_ALL)
            else:
                raise TankError("Channel '%s' doesn't appear to have any layers!" % channel.name())            

        # register the publish:
        progress_cb(80, "Registering the publish")
        args = {
            "tk": self.parent.sgtk,
            "context": self.parent.context,
            "comment": comment,
            "path": publish_path,
            "name": publish_name,
            "version_number": fields["version"],
            "thumbnail_path": thumbnail_path,
            "task": sg_task,
            "published_file_type":output["tank_type"]
        }
        if geo_publish_path:
            args["dependency_paths"] = [geo_publish_path]
        sgtk.util.register_publish(**args)
        
    def __find_publishes(self, ctx, publish_name, publish_type):
        """
        Given a context, publish name and type, find all publishes from Shotgun
        that match.
        
        :param ctx:             Context to use when looking for publishes
        :param publish_name:    The name of the publishes to look for
        :param publish_type:    The type of publishes to look for
        
        :returns:               A list of Shotgun publish records that match the search
                                criteria        
        """
        publish_entity_type = sgtk.util.get_published_file_entity_type(self.parent.sgtk)
        if publish_entity_type == "PublishedFile":
            publish_type_field = "published_file_type.PublishedFileType.code"
        else:
            publish_type_field = "tank_type.TankType.code"
        
        # construct filters from the context:
        filters = [["project", "is", ctx.project]]
        if ctx.entity:
            filters.append(["entity", "is", ctx.entity])
        if ctx.task:
            filters.append(["task", "is", ctx.task])
            
        # add in name & type:
        if publish_name:
            filters.append(["name", "is", publish_name])
        if publish_type:
            filters.append([publish_type_field, "is", publish_type])
            
        # retrieve a list of all matching publishes from Shotgun:
        sg_publishes = []
        try:
            query_fields = ["version_number"]
            sg_publishes = self.parent.shotgun.find(publish_entity_type, filters, query_fields)
        except Exception, e:
            raise TankError("Failed to find publishes of type '%s', called '%s', for context %s: %s" 
                            % (publish_name, publish_type, ctx, e))
        return sg_publishes


