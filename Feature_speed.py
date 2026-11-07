#!/usr/bin/env python3
"""
Feature based speed for 3D prints using klipper firmware.

License: MIT
Author: Benedikt Jansson - WatchingWatches
Version: 1.0
"""
import re
import sys
import traceback

# change the parameters to your liking
WRITE_MACRO: bool = False
PRINT_SPEED_IN_CONSOLE: bool = False
ADD_EXTRUSION: bool = False
# change to your path (needs to be absolute, since the script runs from the slicet)
MACRO_PATH: str = r"C:\Users\bjans\Downloads\Feature_speed.cfg"
type_indicator: str = ';TYPE:'

Travel = re.compile(r"^\s*G[01](?!\d)(?!.*E)", re.IGNORECASE)

Features = []
Features.append("TYPE_TRAVEL")
last_type = ""

def write_macro(line:str)->str:
    """Replace unwanted characters in the line and return the line without them.
    Args:
        line (str): The line to be modified.
    Returns:
        str: The line without unwanted characters and capitalized.
    """
    line = line.replace(" ", "_").replace(":", "_").replace(";", "").replace("\n", "").replace("/","_")
    line = line.upper()

    return line
 
# changes comments to get macros enabled
path = sys.argv[1]
with open(path, 'r') as gcode:
    lines = gcode.readlines()

try:
    with open(path, 'w') as gcode:
        for line in lines:
            old_line = line
            if line.startswith(type_indicator):
                line = write_macro(line)
                last_type = line
                # append when is new type
                if line not in Features:
                    Features.append(line)
                
                line += '\n'
                line += old_line # add the original line relevant for gcode previewer

            elif Travel.match(line):
                line = "TYPE_TRAVEL\n"
                line += old_line  # add the original line relevant for gcode previewer
                if last_type:
                    line += last_type + "\n"  # reset to last kind before travel

            gcode.write(line)

except Exception as e:
    traceback.print_exc()
    input("Press Enter to continue...")

# empty by default when not wanted
extrusion_command = ""
# automatically write the cfg file
if WRITE_MACRO:
    with open(MACRO_PATH, 'w') as cfg:
        cfg.write("# Title: Feature speed macros\n")
        cfg.write("# Source: https://github.com/WatchingWatches/Klipper-Custom-Feature-Speed/tree/main \n")
        for macro in Features:
            # first macro which changes the speed
            cfg.write("[gcode_macro " + macro + "] \n")
            cfg.write("variable_speed_factor: 100 \n")
            if ADD_EXTRUSION:
                cfg.write("variable_extrusion_factor: 100 \n")
            cfg.write("gcode: \n")
            
            cfg.write("    M220 S{"+"speed_factor"+"} \n")
            if ADD_EXTRUSION:
                cfg.write("    M221 S{"+"extrusion_factor"+"} \n")
            
            if PRINT_SPEED_IN_CONSOLE:
                out =  macro + " Speed: {"+"speed_factor"+"}"
                cfg.write("    SHOW_MSG MSG="+"\"{}\"".format(out) + "\n") # check speed with message
            cfg.write("\n")

            # second macro to write to variable
            cfg.write("[gcode_macro SET" + macro[4:] + "_SPEED] \n")
            cfg.write("gcode:\n")
            cfg.write("    {% set speed = params.SPEED|default(100)|int %} \n")
            if ADD_EXTRUSION:
                cfg.write("    {% set extrusion = params.EXTRUSION|default(100)|int %} \n")
                extrusion_command = r"VARIABLE=extrusion_factor VALUE={extrusion}"
            cfg.write("    SET_GCODE_VARIABLE MACRO=" + macro + " VARIABLE=speed_factor VALUE={speed}" + extrusion_command + " \n")
            cfg.write("\n")

        # macro which sets the speed for all features
        cfg.write("[gcode_macro GLOBAL_SPEED] \n")
        cfg.write("description: Set the speed for all features\n")
        cfg.write("gcode:\n")
        cfg.write("    {% set speed = params.SPEED|default(100)|int %} \n")
        for macro in Features:
            cfg.write("    SET_GCODE_VARIABLE MACRO=" + macro + " VARIABLE=speed_factor VALUE={speed}" + extrusion_command + "\n")
        # write speed at the moment
        cfg.write("    M220 S{" + "speed" + "} \n")
        if ADD_EXTRUSION:
            cfg.write("    M221 S{" + "extrusion" + "}")