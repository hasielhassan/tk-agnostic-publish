# tk-agnostic-publish
Shotgun agnostic and standalone app to publish files, but mantaining the structure as the actual tk-multi-publish...

![alt text](https://media.giphy.com/media/3o7TKvpXxxOjGcCbMA/source.gif "Gui Demo")

The main modification to the app relates to the primary output, that now its a list of abailable "editable" files for
a certain context, this allows to match a file extention to a template and from this validate the secondary outputs.

The default configuration could work like this:

```yaml
tk-agnostic-publish:
  allow_taskless_publishes: true
  display_name: Agnostic Publish
  expand_single_items: false
  hook_scan_scene: default
  hook_copy_file: default
  hook_post_publish: default
  hook_primary_pre_publish: default
  hook_primary_publish: default
  hook_secondary_pre_publish: default
  hook_secondary_publish: default
  hook_thumbnail: default
  location:
    path: https://github.com/hasielhassan/tk-agnostic-publish.git
    version: v0.0.1
    type: git
  primary_outputs: 
    - {name: primary,
       extension: c4d,
       icon: icons/publish_cinema_main.png,
       description: "",
       scene_item_type: work_file,
       display_name: Cinema4D Publish,
       tank_type: Cinema4D Scene,
       publish_template: cinema_shot_publish}
    - {name: primary,
       extension: aep,
       icon: icons/publish_after_main.png,
       description: "",
       scene_item_type: work_file,
       display_name: AfterEffects Publish,
       tank_type: AfterEffects Project,
       publish_template: after_shot_publish}
    - {name: primary,
       extension: flw,
       icon: icons/publish_realflow_main.png,
       description: "",
       scene_item_type: work_file,
       display_name: RealFlow Publish,
       tank_type: RealFlow Scene ,
       publish_template: realflow_shot_publish}
  secondary_outputs:
  - {description: After Effects XML Project file, display_group: XML Project,
    display_name: After XML Project, icon: icons/aftereffects_xmlproject.png,
    name: aftereffects_xmlproject, publish_template: after_shot_xml_project_pub,
    required: false, scene_item_type: aftereffects_xmlproject,
    selected: true, tank_type: AfterEffects Project Element}
  - {description: After Effects Project Elements, display_group: Project Elements,
    display_name: After Elements, icon: icons/assets_group_icon.png,
    name: aftereffects_element, publish_template: after_project_element_pub,
    required: false, scene_item_type: aftereffects_element,
    selected: true, tank_type: AfterEffects XML Project}
  - {description: Rendered Sequences, display_group: Renders,
    display_name: Rendered Sequences, icon: icons/publish_nuke_writenode.png,
    name: cinema_render_sequences, publish_template: max_shot_render_publish_exr,
    required: false, scene_item_type: cinema_render_sequences,
    selected: true, tank_type: Cinema4D Render Sequence}
  - {description: Video preview for Shotgun, display_group: Review,
    display_name: Preview Version, icon: icons/publish_global_review.png,
    name: cinema_render_preview_video, publish_template: max_shot_render_publish_mov,
    required: false, scene_item_type: cinema_render_preview_video,
    selected: false, tank_type: Cinema4D Render Preview}
  - {description: Rendered Sequences, display_group: Renders,
    display_name: Rendered Sequences, icon: icons/publish_nuke_writenode.png,
    name: after_render_sequences, publish_template: after_shot_render_pub_exr,
    required: false, scene_item_type: after_render_sequences,
    selected: true, tank_type: AfterEffects Render Sequence}
  - {description: Video preview for Shotgun, display_group: Review,
    display_name: Preview Version, icon: icons/publish_global_review.png,
    name: after_render_preview_video, publish_template: after_shot_render_pub_preview,
    required: false, scene_item_type: after_render_preview_video,
    selected: false, tank_type: AfterEffects Render Preview}
  template_work: max_shot_work
```

That will need the following templates:

```yaml
max_shot_render_publish_exr
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Renders/{name}/v{version}/{set_name}/scn{shot_scene_name}_sht{Shot}_{step_code}_{set_name}_v{version}.{buffer}.{SEQ}.exr'

max_shot_render_publish_mov
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Renders/{name}/v{version}/{set_name}/scn{shot_scene_name}_sht{Shot}_{step_code}_{set_name}_v{version}_{buffer}.mov'


after_shot_publish
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Editables/scn{shot_scene_name}_sht{Shot}_{step_code}_{name}_v{version}.aep'

cinema_shot_publish
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Editables/scn{shot_scene_name}_sht{Shot}_{step_code}_{name}_v{version}.c4d'


after_project_element_pub
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Elements/scn{shot_scene_name}_sht{Shot}_{step_code}_{name}_{element_file_name}_v{version}.{extension}'

after_shot_xml_project_pub
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/XMLProjects/scn{shot_scene_name}_sht{Shot}_{step_code}_{name}_v{version}.aepx'


after_shot_render_pub_exr
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Renders/{name}/v{version}/{comp_name}/scn{shot_scene_name}_sht{Shot}_{step_code}_{name}_{comp_name}_v{version}.{SEQ}.exr'

after_shot_render_pub_preview
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Previews/{name}/scn{shot_scene_name}_sht{Shot}_{step_code}_{name}_{comp_name}_v{version}.mov'

realflow_shot_publish
  definition: '@publish_shot_root/scn{shot_scene_name}/sht{Shot}/Editables/scn{shot_scene_name}_sht{Shot}_{step_code}_{name}_v{version}.flw'
```
It also require the followin dependencies:

 - pyseq - For file sequence detection 
 - ffmpeg - For transcoding
 - imagemgick - To deal with linear vs sRGB images
