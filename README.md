# Klipper Custom Feature Speed
## Introduction:
This postprocessing script in combination with a Klipper macro enables the user to change the printing speed based on the printed feature type.
The printing speed is changed with an M220 command, which changes the printing speed by a given factor. 
The script works with prusa and orca slicer, but can be adopted to other slicers, which also use comments within the gcode to indicate a feature type.

### Why would you want to use this?
There are a few scenarios, when you might want to use this:
1. You want to increase the printing speed, which means there will be less part cooling. Overhang/bridging structures need to be printed slower to ensure good cooling. You can increase the overall speed with the ``GLOBAL_SPEED`` and then set the ``SET_OVERHANG_PERIMETER_SPEED`` to 100% to use the original speed set by the slicer.
2. During the print the supports nearly tip over, so you want to lower the printing speed. However the rest of the print is totally fine and you don't want to increase the printing time of the whole print, just because of the supports.
3. One specific feature is printed at the wrong speed, because you set a wrong speed in the slicer. With this macro you can fix your mistake.

In general it's recommended to set the right printing speeds in your slicer, which considers many factors to calculate the printing speed. This tool gives advanced options to change the printing speed during the print. Only use reasonable factors.

Every time a new feature is printed the printing speed is overwritten with a new factor. This means, that you can't use the normal M220 command anymore, since it will be overwritten by the macro's.
Use ``GLOBAL_SPEED`` instead, which works like the old M220 command.

## How to set up:
1. Set ``Feature_speed.py`` as a postprocessing script in your slicer [here is a guide](https://github.com/WatchingWatches/Post_processing_gcode?tab=readme-ov-file#how-to-run-script-from-slic3rprusaslicerorcaslicer)

2. Optional Generate the macro. There are already two files available for orca and prusa slicer (i can't guarantee, that every feature type is included):
- set ``MACRO_PATH`` to a path on your computer and set ``WRITE_MACRO = True``
- check that the comment in the gcode indicating the feature type starts with ``;TYPE:``
if it's different in your slicer change ``if line.startswith(';TYPE:'):`` to match the beginning of the comment.
The beginning of the line needs to be always the same. 
- save a gcode file from your slicer, which includes every feature type available in the slicer. The macro will be written automatically to the given path.

3. Include the macro in your printer config: 
- create a new file in your config folder and copy the macro file for your slicer
- include the file in your ``printer.cfg``
- add ``[respond]`` to your ``printer.cfg`` if you haven't included it already
- add the SET_ macros to your macros (i recommend to create a new group)

Once you have set up everything you don't need to do anything else when slicing. Just remember to add the postprocessing script to every profile you are using.
The postprocessing script is very simple and doesn't take much execution time. 
You can set ``WRITE_MACRO = False`` after the first setup. 

If you need help with the setup just open an issue here on Github.
Keep in mind, that updates of the slicer might bring new feature types.

## Advanced possibilities:
You could add additional options to the script to enable a custom acceleration, extrusion factor, firmware retraction...  
The options are endless, but might be very specific to your needs.
If you would like to add these kind of options it's recommended to use the python script to adapt the generated macros.
If you have ideas for useful options and need help adding those open an issue.
If you want to contribute to this project open a pull request.
