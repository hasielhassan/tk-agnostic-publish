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
import mari

import tank
from tank import Hook
from tank import TankError

class ScanSceneHook(Hook):
    """
    Hook to scan scene for items to publish
    """
    
    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       A list of any items that were found to be published.  
                        Each item in the list should be a dictionary containing 
                        the following keys:
                        {
                            type:   String
                                    This should match a scene_item_type defined in
                                    one of the outputs in the configuration and is 
                                    used to determine the outputs that should be 
                                    published for the item
                                    
                            name:   String
                                    Name to use for the item in the UI
                            
                            description:    String
                                            Description of the item to use in the UI
                                            
                            selected:       Bool
                                            Initial selected state of item in the UI.  
                                            Items are selected by default.
                                            
                            required:       Bool
                                            Required state of item in the UI.  If True then
                                            item will not be deselectable.  Items are not
                                            required by default.
                                            
                            other_params:   Dictionary
                                            Optional dictionary that will be passed to the
                                            pre-publish and publish hooks
                        }
        """   
                
        items = []
        
        # check that we are currently inside a project:
        if not mari.projects.current():
            raise TankError("You must be in an open Mari project to be able to publish!")
        
        # Mari doesn't have a primary publish item at the moment so
        # just add a dummy item to keep the app happy:
        items.append({"type":"work_file", "name":None})

        # Look for all layers for all channels on all geometry.  Create items for both
        # the flattened channel as well as the individual layers
        for geo in mari.geo.list():
            for channel in geo.channelList():

                params = {"geo":geo.name(), "channel":channel.name()}

                # find all publishable layers:
                publishable_layers = self.find_publishable_layers_r(channel.layerList())
                if not publishable_layers:
                    # no layers to publish!
                    continue

                # add item for whole flattened channel:
                item_name = "%s, %s" % (geo.name(), channel.name())
                items.append({"type":"channel", "name":item_name, "other_params":params})
                
                # add item for each publishable layer:
                found_layer_names = set()
                for layer in publishable_layers:
                    
                    # for now, duplicate layer names aren't allowed!
                    layer_name = layer.name()
                    if layer_name in found_layer_names:
                        # we might want to handle this one day...
                        pass
                    found_layer_names.add(layer_name)
                    
                    # add item for channel layer:
                    item_name = "%s, %s (%s)" % (geo.name(), channel.name(), layer_name)
                    params = {"geo":geo.name(), "channel":channel.name(), "layer":layer_name}                    
                    items.append({"type":"layer", "name":item_name, "other_params":params})

        return items

    def find_publishable_layers_r(self, layers):
        """
        Find all publishable layers within the specified list of layers.  This will return
        all layers that are either paintable or procedural and traverse any layer groups
        to find all grouped publishable layers

        :param layers:  The list of layers to inspect
        :returns:       A list of all publishable layers
        """
        publishable = []
        for layer in layers:
            # Note, only paintable or procedural layers are exportable from Mari - all
            # other layer types are only used within Mari.
            if layer.isPaintableLayer() or layer.isProceduralLayer():
                # these are the only types of layers that are publishable
                publishable.append(layer)
            elif layer.isGroupLayer():
                # recurse over all layers in the group looking for exportable layers:
                grouped_layers = self.find_publishable_layers_r(layer.layerStack().layerList())
                publishable.extend(grouped_layers or [])
    
        return publishable









