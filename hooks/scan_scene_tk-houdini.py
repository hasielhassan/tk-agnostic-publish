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
import hou

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

        if hou.hipFile.name() == "untitled.hip":
            raise TankError("Please save your file before Publishing")

        # get the main scene:
        scene_name = str(hou.hipFile.name())
        scene_path = os.path.abspath(scene_name)
        name = os.path.basename(scene_path)

        # create the primary item - this will match the primary output 'scene_item_type':
        items.append({"type": "work_file", "name": name})

        # look for alembic caches to publish
        items.extend(self._get_alembic_items())

        # look for rendered images to publish
        items.extend(self._get_rendered_image_items())

        return items

    def _get_alembic_items(self):
        """Scan the file for tk alembic nodes to potentially publish."""

        app = self.parent
        
        # see if the alembicnode app is installed
        alembic_app = app.engine.apps.get("tk-houdini-alembicnode", None)
        if not alembic_app:
            app.log_info(
                "Will not attempt to scan for alembic caches."
                "The 'tk-houdini-alembicnode' app is not installed."
            )
            return []

        # get all the tk alembic nodes in the scene
        tk_alembic_nodes = hou.nodeType(hou.ropNodeTypeCategory(),
            "sgtk_alembic").instances()

        alembic_items = []

        # add all tk alembic nodes to the list of secondary publish items.
        for tk_alembic_node in tk_alembic_nodes:

            is_bypassed = tk_alembic_node.isBypassed()

            out_path_parm = tk_alembic_node.parm("filename")
            out_path = out_path_parm.menuLabels()[out_path_parm.eval()]

            # normalize the path
            out_path = os.path.normpath(out_path)

            # only select the item if the path exists and the node is not
            # bypassed
            should_select = out_path and os.path.exists(out_path) and \
                not is_bypassed

            alembic_items.append({
                "name": tk_alembic_node.name(),
                "type": "alembic_cache",
                "description": "Full Path: %s" % (tk_alembic_node.path(),),
                "selected": should_select,
                "other_params": {
                    "path": out_path,
                    "node": tk_alembic_node,
                },
            })

        return alembic_items

    def _get_rendered_image_items(self):
        """Scan the file for tk mantra nodes to potentially publish."""

        app = self.parent

        # see if the mantranode app is installed
        mantra_app = app.engine.apps.get("tk-houdini-mantranode", None)
        if not mantra_app:
            app.log_info(
                "Will not attempt to scan for rendered images."
                "The 'tk-houdini-mantranode' app is not installed."
            )
            return []

        # find all the tk mantra nodes
        tk_mantra_nodes = hou.nodeType(hou.ropNodeTypeCategory(),
            "sgtk_mantra").instances()

        render_items = []

        # get the current version from the work file
        work_template = mantra_app.get_template("work_file_template")
        scene_name = str(hou.hipFile.name())
        scene_path = os.path.abspath(scene_name)
        fields = work_template.get_fields(scene_path)
        cur_version = fields["version"]
        fields["SEQ"] = "FORMAT: %d"

        # get the output_profiles for the app. More efficient to do this here
        # than to repeat this logic per item in the secondary publish hook.
        output_profiles = {}
        for output_profile in mantra_app.get_setting("output_profiles"):
            name = output_profile["name"]
            output_profiles[name] = output_profile

        # for each mantra node, see which output profile is selected.
        # get the template for the selected profile. the validation hook will
        # check see if there are any images on disk matching the pattern
        for tk_mantra_node in tk_mantra_nodes:

            output_profile_parm = tk_mantra_node.parm("sgtk_output_profile")
            output_profile_name = \
                output_profile_parm.menuLabels()[output_profile_parm.eval()]
            output_profile = output_profiles[output_profile_name]
            output_template = mantra_app.get_template_by_name(
                output_profile["output_render_template"])

            is_bypassed = tk_mantra_node.isBypassed()

            paths = mantra_app.engine.tank.abstract_paths_from_template(
                output_template, fields)

            # normalize the paths
            paths = [os.path.normpath(p) for p in paths]

            # only select the item if the output path exists and the node is
            # not bypassed.
            should_select = len(paths) == 1 and not is_bypassed

            render_items.append({
                "type": "rendered_image",
                "name": tk_mantra_node.name(),
                "description": "Full Path: %s" % (tk_mantra_node.path(),),
                "selected": should_select,
                "other_params": {
                    "paths": paths,
                    "node": tk_mantra_node,
                },
            })

        return render_items

