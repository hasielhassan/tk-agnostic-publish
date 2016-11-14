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
import pyseq
import traceback

import sgtk
from sgtk import Hook
from sgtk import TankError
from tank.platform.qt import QtCore, QtGui

import xml.etree.ElementTree as ET


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

        # create the primary item - 'type' should match the 'primary_scene_item_type':

        if self.parent.agnostic_scene_contents['primary'] != None:

            input_dict = self.parent.agnostic_scene_contents['primary']

            if self.parent.initialized_from == "primary":
                self.parent.context_fields = self.process_fields(input_dict)

            scene_path = input_dict['output'].publish_template.apply_fields(self.parent.context_fields)
            items.append({"type": "work_file",
                          "name": os.path.basename(scene_path),
                          'other_params': {'source': input_dict['path'],
                                           'destination': scene_path}})

        items.extend(self.scan_for_render_sequences(self.parent.agnostic_scene_contents['secondary']))

        items.extend(self.scan_for_after_xml(self.parent.agnostic_scene_contents['secondary']))

        return items

    def scan_for_after_xml(self, inputs):

        items = []


        if len(self.parent.agnostic_scene_contents['secondary']) != 0:

            if self.parent.agnostic_scene_contents['primary']['output'].extension in ['aep']:
            
                for input_dict in inputs:
                    dirname_filename, extension = os.path.splitext(input_dict['path'])
                    if input_dict['class'] == 'single' and extension.lower() == '.aepx':

                        #<AfterEffectsProject xmlns="http://www.adobe.com/products/aftereffects" majorVersion="1" minorVersion="0">
                        ET.register_namespace('', "http://www.adobe.com/products/aftereffects")
                        after_tree = ET.parse(input_dict['path'])

                        #first process itput references
                        references = self.after_recurse_get_fileReference(after_tree.getroot())

                        #store a dictionary for each reference file with source and publish paths to later replace it in the xml file
                        references_dict = {}
                        processed_paths = []

                        for ref in references:

                            after_element_template = self.parent.sgtk.templates['after_project_element_pub']
                            reference_fields = dict(self.parent.context_fields)

                            if ref['fullpath'] not in references_dict and ref['fullpath'] not in processed_paths:

                                self.parent.log_debug("Testing:")
                                self.parent.log_debug(ref['fullpath'])

                                if ref['filetype'] != 'fffffffe':
                                    #The input reference its not an image sequence (folder)
                                    self.parent.log_debug(sgtk.util.find_publish(self.parent.sgtk, [ref['fullpath']]))

                                    if not sgtk.util.find_publish(self.parent.sgtk, [ref['fullpath']]):

                                        name, ext = os.path.splitext(os.path.basename(ref['fullpath']))
                                        ref_name = self.beautify_name(name)

                                        reference_fields['element_file_name'] = ref_name
                                        reference_fields['extension'] = ext[1:]

                                        publish_path = after_element_template.apply_fields(reference_fields)

                                        items.append({"type": "aftereffects_element",
                                                      "name": "%s (%s)" % (os.path.basename(ref['fullpath']), os.path.basename(publish_path)),
                                                      "other_params": {'item_dict': {'path': ref['fullpath'], 'class': 'single'},
                                                                       'fields': reference_fields,
                                                                       'publish_path': publish_path,
                                                                       'publish_template': after_element_template}})

                                        references_dict[ref['fullpath']] = publish_path

                                    else:
                                        processed_paths.append(ref['fullpath'])

                                else:
                                    #The input reference its an image sequence (folder)
                                    if os.path.exists(ref['fullpath']):

                                        sequences = pyseq.get_sequences(ref['fullpath'])

                                        if len(sequences) != 0:
                                            for seq in sequences:
                                                seq_format = os.path.join(os.path.dirname(seq.path()), seq.format("%h%p%t"))

                                                #validate if exclusively corresponds to a padded sequence

                                                if "%" in seq_format:

                                                    if not sgtk.util.find_publish(self.parent.sgtk, [seq_format]):

                                                        #Its complex to provide an ideal way to store this files
                                                        self.parent.log_debug(seq_format)



                        #add xml project item
                        after_xml_template = self.parent.sgtk.templates['after_shot_xml_project_pub']
                        publish_path = after_xml_template.apply_fields(self.parent.context_fields)
                        items.append({"type": "aftereffects_xmlproject",
                                      "name": "%s (%s)" % (os.path.basename(input_dict['path']), os.path.basename(publish_path)),
                                      "other_params": {'item_dict': input_dict,
                                                       'xml_tree': after_tree,
                                                       'references_dict': references_dict,
                                                       'fields': self.parent.context_fields,
                                                       'publish_path': publish_path,
                                                       'publish_template': after_xml_template}})


        return items


    def scan_for_render_sequences(self, inputs):

        items = []

        if len(self.parent.agnostic_scene_contents['secondary']) != 0:
            

            for input_dict in inputs:
                dirname_filename, extension = os.path.splitext(input_dict['path'])
                if input_dict['class'] == 'sequence' and extension.lower() == '.exr':

                    if self.parent.agnostic_scene_contents['primary']['output'].extension in ['c4d']:

                        cinema_work_render_template = self.parent.sgtk.templates['cinema_shot_render_work_exr']
                        cinema_publish_render_template = self.parent.sgtk.templates['max_shot_render_publish_exr']
                        cinema_publish_preview_template = self.parent.sgtk.templates['max_shot_render_publish_mov']

                        if cinema_work_render_template.validate(input_dict['path']):

                            work_fields = cinema_work_render_template.get_fields(input_dict['path'])                            
                            all_fields = self.complete_fields(input_dict['path'], work_fields, cinema_publish_render_template)                            

                            #only save the item if the user fill all the missing keys
                            if all_fields:

                                #append render sequence item
                                publish_path = cinema_publish_render_template.apply_fields(all_fields)
                                items.append({"type": "cinema_render_sequences",
                                              "name": "%s (%s)" % (os.path.basename(input_dict['path']), os.path.basename(publish_path)),
                                              "other_params": {'item_dict': input_dict,
                                                               'fields': all_fields,
                                                               'publish_path': publish_path,
                                                               'work_template': cinema_work_render_template,
                                                               'publish_template': cinema_publish_render_template}})

                                #append render preview item
                                preview_path = cinema_publish_preview_template.apply_fields(all_fields)
                                #override input dict path to reflect the published one
                                preview_input_dict = dict(input_dict)
                                preview_input_dict['path'] = publish_path
                                items.append({"type": "cinema_render_preview_video",
                                              "name": "%s (%s)" % (os.path.basename(input_dict['path']), os.path.basename(preview_path)),
                                              "other_params": {'item_dict': input_dict,
                                                               'fields': all_fields,
                                                               'publish_path': preview_path,
                                                               'work_template': cinema_work_render_template,
                                                               'publish_template': cinema_publish_preview_template}})


                    if self.parent.agnostic_scene_contents['primary']['output'].extension in ['aep']:

                        after_work_render_template = self.parent.sgtk.templates['after_shot_render_work_exr']
                        after_publish_render_template = self.parent.sgtk.templates['after_shot_render_pub_exr']
                        after_publish_preview_template = self.parent.sgtk.templates['after_shot_render_pub_preview']

                        if after_work_render_template.validate(input_dict['path']):

                            work_fields = after_work_render_template.get_fields(input_dict['path'])                            
                            all_fields = self.complete_fields(input_dict['path'], work_fields, after_publish_render_template)                            

                            #only save the item if the user fill all the missing keys
                            if all_fields:

                                #append render sequence item
                                publish_path = after_publish_render_template.apply_fields(all_fields)
                                items.append({"type": "after_render_sequences",
                                              "name": "%s (%s)" % (os.path.basename(input_dict['path']), os.path.basename(publish_path)),
                                              "other_params": {'item_dict': input_dict,
                                                               'fields': all_fields,
                                                               'publish_path': publish_path,
                                                               'work_template': after_work_render_template,
                                                               'publish_template': after_publish_render_template}})

                                #append render preview item
                                preview_path = after_publish_preview_template.apply_fields(all_fields)
                                #override input dict path to reflect the published one
                                preview_input_dict = dict(input_dict)
                                preview_input_dict['path'] = publish_path
                                items.append({"type": "after_render_preview_video",
                                              "name": "%s (%s)" % (os.path.basename(input_dict['path']), os.path.basename(preview_path)),
                                              "other_params": {'item_dict': input_dict,
                                                               'fields': all_fields,
                                                               'publish_path': preview_path,
                                                               'work_template': after_work_render_template,
                                                               'publish_template': after_publish_preview_template}})
                            else:
                                self.parent.log_debug("Skiping path: %s because can't fill its fields for template: %s" % (input_dict['path'], after_work_render_template))


                        else:
                            self.parent.log_debug("Skiping path: %s because dont match template: %s" % (input_dict['path'], after_work_render_template))


        return items


    def beautify_name(self, base_string):

        """
        Method to translate a string with spaces, dashes, and other simbols into a camel case one
        """

        tokens = [base_string]
        for sep in [' ', '-', '_', '.']:
            base_string, tokens = tokens, []
            for seq in base_string:
                tokens += seq.split(sep)

        tokens = [element.title() for element in tokens]

        camel_case_string = "".join(tokens)

        return camel_case_string



    def complete_fields(self, input_path, current_fields, target_template):

        """
        """

        all_fields = dict(current_fields)

        for key in target_template.keys:

            if key not in current_fields:

                if key in self.parent.context_fields:

                    all_fields[key] = self.parent.context_fields[key]

                else:
                    message = 'Enter the %s token for your published files:\n%s\n' % (key, input_path)
                    field_input, responce = QtGui.QInputDialog.getText(None, 'Complete Fields', message)
                    if responce:
                        all_fields[key] = field_input.replace(' ', '').replace('-', '').replace('_', '').lower()
                    else:
                        return None

        return all_fields


    def process_fields(self, input_dict):

        # get scene path
        fields = self.parent.context.as_template_fields(input_dict['output'].publish_template, self.parent.context)

        if 'name' in input_dict['output'].publish_template.keys:
            name_input, responce = QtGui.QInputDialog.getText(None, 'Publish Name', 'Enter the name token for your published files:', text=u'master')
            if responce:
                fields['name'] = name_input.replace(' ', '').replace('-', '').replace('_', '').lower()
            else:
                return items

        if 'version' in input_dict['output'].publish_template.keys:
            version = self.compute_highest_version(self.parent.sgtk, input_dict['output'].publish_template, fields)
            fields['version'] = version + 1

        return fields


    def compute_highest_version(self, sgtk, template, curr_fields):
        """
        Given a template and some fields, return the highest version number found on disk.
        The template key containing the version number is assumed to be named {version}.
        
        This will perform a scan on disk to determine the highest version.
        
        :param sgtk: tank api instance for a project
        :param template: Template object to calculate for
        :param curr_fields: A complete set of fields for the template
        :returns: The highest version number found
        """
        # set up the payload
        output = {}

        # calculate visibility
        # check if this is the latest item

        # note - have to do some tricks here to get sequences and stereo working
        # need to fix this in Tank platform

        # get all eyes, all frames and all versions
        # potentially a HUGE glob, so may be slow...
        # todo: better support for sequence iterations
        #       by using the abstract iteration methods
        
        # first, find all abstract (Sequence) keys from the template:
        abstract_keys = set()
        for key_name, key in template.keys.iteritems():
            if key.is_abstract:
                abstract_keys.add(key_name)

        # skip keys are all abstract keys + 'version' & 'eye'
        skip_keys = [k for k in abstract_keys] + ["version", "eye"]

        # then find all files, skipping these keys
        all_versions = sgtk.paths_from_template(template, curr_fields, skip_keys=skip_keys)

        # if we didn't find anything then something has gone wrong with our 
        # logic as we should have at least one file so error out:
        # TODO - this should be handled more cleanly!
        if not all_versions:
            print "Failed to find any files!"   
        
        # now look for the highest version number...
        highest_version = 0
        for ver in all_versions:
            curr_fields = template.get_fields(ver)
            if curr_fields["version"] > highest_version:
                highest_version = curr_fields["version"]

        return highest_version



    def after_recurse_get_fileReference(self, element):
        """
        Method to collect all fileReference items in the xml proyect
        """
        for child in element.getchildren():

            if 'fileReference' in child.tag:
                yield { key: value for key, value in child.attrib.iteritems()}

            for item in self.after_recurse_get_fileReference(child):
                yield item
