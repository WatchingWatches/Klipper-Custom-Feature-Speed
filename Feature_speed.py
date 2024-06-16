#!/usr/bin/env python3
"""
Feature based speedfor 3D prints using klipper firmware.

License: MIT
Author: Benedikt Jansson - WatchingWatches
Version: 1.0
"""
import sys
import traceback

WRITE_MACRO = True
# change to your path
MACRO_PATH = r"C:\Users\bjans\OneDrive\Dokumente\CAD\Software\post_processing_gcode\Feature_speed_macro\Feature_speed.cfg"

Features = []

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
            if line.startswith(';TYPE:'):
                old_line = line
                line = write_macro(line) 
                # append when is new type
                if line not in Features:
                    Features.append(line)
                
                line += '\n'
                line += old_line # add the original line relevant for gcode previewer

            gcode.write(line)

except Exception as e:
    traceback.print_exc()
    input("Press Enter to continue...")


# automatically write the cfg file
if WRITE_MACRO:
    with open(MACRO_PATH, 'w') as cfg:
        cfg.write("# Title: Feature speed macros\n")
        for i,macro in enumerate(Features):
            cfg.write("[gcode_macro " + macro + "] \n")
            cfg.write("variable_speed_factor: 100\n")
            cfg.write("gcode:\n")
            #name = "SPEED_"+ str(i) 
            
            cfg.write("    M220 S{"+"speed_factor"+"}\n")
            # can be deleted later
            out =  macro + " Speed: {"+"speed_factor"+"}"
            cfg.write("    SHOW_MSG MSG="+"\"{}\"".format(out) + "\n") #check speed with message
            cfg.write("\n")

            # second macro to write to variable
            cfg.write("[gcode_macro SET" + macro[4:] + "_SPEED] \n")
            cfg.write("gcode:\n")
            cfg.write("    {% set speed = params.SPEED|default(100)|int %} \n")
            cfg.write("    SET_GCODE_VARIABLE MACRO="+ macro + " VARIABLE=speed_factor VALUE={speed}\n")
            cfg.write("\n")

        # macro which sets the speed for all features
        cfg.write("[gcode_macro GLOBAL_SPEED] \n")
        cfg.write("description: Set the speed for all features\n")
        cfg.write("gcode:\n")
        cfg.write("    {% set speed = params.SPEED|default(100)|int %} \n")
        for macro in Features:
            cfg.write("    SET_GCODE_VARIABLE MACRO="+ macro + " VARIABLE=speed_factor VALUE={speed}\n")
        # write speed at the moment
        cfg.write("    M220 S{" + "speed" + "}")