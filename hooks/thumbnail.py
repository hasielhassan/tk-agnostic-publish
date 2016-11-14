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
import tempfile
import uuid
import re

import tank
from tank import Hook

class ThumbnailHook(Hook):
    """
    Hook that can be used to provide a pre-defined primary 
    thumbnail for the publish
    """
    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       String
                        Hook should return a file path pointing to the location of
                        a thumbnail file on disk that will be used for the publish.
                        If the hook returns None then the screenshot functionality
                        will be enabled in the UI.
        """
        # get the engine name from the parent object (app/engine/etc.)
        engine = self.parent.engine
        engine_name = engine.name
        
        # depending on engine:
        if engine_name == "tk-nuke":
            return self._extract_nuke_thumbnail()
        elif engine_name == "tk-hiero":
            return self._extract_hiero_thumbnail()
        elif engine_name == "tk-photoshop":
            return self._extract_photoshop_thumbnail()
        elif engine_name == "tk-mari":
            return self._extract_mari_thumbnail()

        # default implementation does nothing        
        return None
    
    def _extract_mari_thumbnail(self):
        """
        Render a thumbnail for the current canvas in Mari
        
        :returns:   The path to the thumbnail on disk
        """
        import mari
        if not mari.projects.current():
            return
        
        canvas = mari.canvases.current()
        if not canvas:
            return
        
        # calculate the maximum size to capture:
        MAX_THUMB_SIZE = 512
        sz = canvas.size()
        thumb_width = sz.width()
        thumb_height = sz.height()
        max_sz = max(thumb_width, sz.height())
    
        if max_sz > MAX_THUMB_SIZE:
            scale = min(float(MAX_THUMB_SIZE)/float(max_sz), 1.0)
            thumb_width = max(min(int(thumb_width * scale), thumb_width), 1)
            thumb_height = max(min(int(thumb_height * scale), thumb_height), 1)
    
        # disable the HUD:
        hud_enabled = canvas.getDisplayProperty("HUD/RenderHud")
        if hud_enabled:
            # Note - this doesn't seem to work when capturing an image!
            canvas.setDisplayProperty("HUD/RenderHud", False)

        # render the thumbnail:
        thumb = None
        try:    
            thumb = canvas.captureImage(thumb_width, thumb_height)
        except:
            pass
        
        # reset the HUD
        if hud_enabled:
            canvas.setDisplayProperty("HUD/RenderHud", True)
        
        if thumb:
            # save the thumbnail
            png_thumb_path = os.path.join(tempfile.gettempdir(), "sgtk_thumb_%s.png" % uuid.uuid4().hex)
            thumb.save(png_thumb_path)
        
        return png_thumb_path

    def _extract_nuke_thumbnail(self):
        """
        Render a thumbnail from the first valid sequence in supported Nuke modes.

        :returns:   The path to the thumbnail on disk
        """
        engine = self.parent.engine

        if hasattr(engine, "hiero_enabled") and engine.hiero_enabled:
            return self._extract_hiero_thumbnail()
        elif hasattr(engine, "studio_enabled") and engine.studio_enabled:
            return self._extract_nukestudio_thumbnail()
        else:
            # This means we're in Nuke, which we won't do anything with.
            return None

    def _extract_nukestudio_thumbnail(self):
        """
        Render a thumbnail from the first valid sequence in Nuke Studio.

        :returns:   The path to the thumbnail on disk
        """
        # We treat Nuke Studio exactly like Hiero out of the box.
        return self._extract_hiero_thumbnail()
    
    def _extract_hiero_thumbnail(self):
        """
        Render a thumbnail from the first valid sequence in Hiero.

        :returns:   The path to the thumbnail on disk
        """
        import hiero.core
        from PySide import QtCore
        
        # get the menu selection from hiero engine
        selection = self.parent.engine.get_menu_selection()

        if len(selection) != 1:
            raise TankError("Please select a single Project!")
        
        if not isinstance(selection[0] , hiero.core.Bin):
            raise TankError("Please select a Hiero Project!")
            
        project = selection[0].project()
        if project is None:
            # apparently bins can be without projects (child bins I think)
            raise TankError("Please select a Hiero Project!")
        
        # find first sequence with a poster frame
        for s in project.sequences():            
            if s.posterFrame():
                try:
                    # this sequence has got a poster frame!
                    thumb_qimage = s.thumbnail(s.posterFrame())
                    # scale it down to 600px wide
                    thumb_qimage_scaled = thumb_qimage.scaledToWidth(600, QtCore.Qt.SmoothTransformation)
                    # save it to tmp location
                    png_thumb = os.path.join(tempfile.gettempdir(), "sgtk_thumb_%s.png" % uuid.uuid4().hex)
                    thumb_qimage_scaled.save(png_thumb)
                    return png_thumb
                except:
                    return None
        
        return None

    def _extract_photoshop_thumbnail(self):
        """
        Extract a thumbnail from the current doc in Photoshop
        
        :returns:   The path to the thumbnail on disk
        """
        import photoshop
        MAX_THUMB_SIZE = 512

        # set unit system to pixels:
        original_ruler_units = photoshop.app.preferences.rulerUnits
        pixel_units = photoshop.StaticObject('com.adobe.photoshop.Units', 'PIXELS')
        photoshop.app.preferences.rulerUnits = pixel_units        

        try:
            active_doc = photoshop.app.activeDocument
            orig_name = active_doc.name
            width_str = active_doc.width
            height_str = active_doc.height
            
            # build temp name for the thumbnail doc (just in case we fail to close it!):
            name, sfx = os.path.splitext(orig_name)
            thumb_name = "%s_tkthumb.%s" % (name, sfx)
            
            # find the doc size in pixels
            # Note: this doesn't handle measurements other than pixels.
            doc_width = doc_height = 0
            exp = re.compile("^(?P<value>[0-9]+) px$")
            mo = exp.match (width_str)
            if mo:
                doc_width = int(mo.group("value"))
            mo = exp.match (height_str)
            if mo:
                doc_height = int(mo.group("value"))
    
            thumb_width = thumb_height = 0
            if doc_width and doc_height:
                max_sz = max(doc_width, doc_height)
                if max_sz > MAX_THUMB_SIZE:
                    scale = min(float(MAX_THUMB_SIZE)/float(max_sz), 1.0)
                    thumb_width = max(min(int(doc_width * scale), doc_width), 1)
                    thumb_height = max(min(int(doc_height * scale), doc_height), 1)
    
            # get a path in the temp dir to use for the thumbnail:
            png_pub_path = os.path.join(tempfile.gettempdir(), "%s_sgtk.png" % uuid.uuid4().hex)
            
            # get a file object from Photoshop for this path and the current PNG save options:
            thumbnail_file = photoshop.RemoteObject('flash.filesystem::File', png_pub_path)
            png_options = photoshop.RemoteObject('com.adobe.photoshop::PNGSaveOptions')
    
            # duplicate the original doc:
            save_options = photoshop.flexbase.requestStatic('com.adobe.photoshop.SaveOptions', 'DONOTSAVECHANGES')        
            thumb_doc = active_doc.duplicate(thumb_name)
    
            try:
                # flatten image:
                thumb_doc.flatten()            
                
                # resize if needed:
                if thumb_width and thumb_height:
                    thumb_doc.resizeImage("%d px" % thumb_width, "%d px" % thumb_height)            
            
                # save:
                thumb_doc.saveAs(thumbnail_file, png_options, True)
    
            finally:
                # close the doc:
                thumb_doc.close(save_options)
                
            return png_pub_path
                        
        finally:
            # set units back to original
            photoshop.app.preferences.rulerUnits = original_ruler_units

