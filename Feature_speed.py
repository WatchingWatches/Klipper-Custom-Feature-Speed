import sys
import traceback

WRITE_MACRO = True
MACRO_PATH = r"C:\Users\bjans\OneDrive\Dokumente\CAD\Software\post_processing_gcode\Feature_speed_macro\Feature_speed.cfg"

Features = []

def write_macro(line:str)->str:
    """Replace unwanted characters in the line and return the line without them.
    Args:
        line (str): The line to be modified.
    Returns:
        str: The line without unwanted characters.
    """
    line = line.replace(" ", "_").replace(":", "_").replace(";", "").replace("\n", "").replace("/","_")
    # nur grßbuchstaben???
    return line
    
# changes comments to get macros enabled
path = sys.argv[1]
with open(path, 'r') as gcode:
    lines = gcode.readlines()
gcode.close()

try:
    with open(path, 'w') as gcode:
        for line in lines:
            if line.startswith(';TYPE:'):
                line = write_macro(line)
                # append when is new type
                if line not in Features:
                    Features.append(line)

            gcode.write(line)

except Exception as e:
    traceback.print_exc()

# TODO testen ob flow zurückgesetzt wird jedes mal wenn gecalled wird
# automatically write the cfg file
if WRITE_MACRO:
    with open(MACRO_PATH, 'w') as cfg:
        for i,macro in enumerate(Features):
            cfg.write("[gcode_macro " + macro + "] \n")
            cfg.write("gcode:\n")
            name = "SPEED_"+ str(i) 
            cfg.write("    {% set "+ name +" = params."+ name +"|default(100)|int %} \n")
            cfg.write("    M220 S{"+ name +"}\n")
            out =  macro + " Speed: {"+ name +"}"
            cfg.write("    SHOW_MSG MSG="+"\"{}\"".format(out) + "\n") #check speed with message
            cfg.write("\n")