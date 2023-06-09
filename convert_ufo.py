## Author: NightFurySL2001 (https://github.com/NightFurySL2001/py-fonttools-script)
## Copyright © 2022 NightFurySL2001 (NFSL2001)
## Released under MIT License

import extractor
import defcon
import sys
import os

import argparse

def check_font(fontname):
    if fontname.lower().endswith((".ttf",".otf")):
        return fontname
    else:
        raise TypeError("Not a font file.")

parser = argparse.ArgumentParser(description='Convert an input font (TTF/OTF) to UFO format.')

parser.add_argument('fontname', type=check_font, help="Input of font path")
parser.add_argument('-f', '--folder', help="Output folder path. If none is given it will try to detect the folder the file is in, else save it in the folder where the program is located.")
parser.add_argument('-o', '--outputname', help="")
parser.add_argument('-z', '--zip', action="store_true")

if sys.argv[0].endswith((".py",".exe")):
    sys.argv.pop(0) #remove current running script from list of args

variables = parser.parse_args(sys.argv)

#font name as parameter 1
fontname = variables.fontname
#save structure
structure = "zip" if variables.zip else "package"

#folder name as parameter 2
if variables.folder is not None:
    folder = variables.folder
else:
    if os.path.isabs(fontname):
        folder = os.path.dirname(fontname)
    else:
        folder = "."

#if folder not exist
if not os.path.isdir(folder):
    os.mkdir(folder)

#check output font name
if variables.outputname is not None:
    outputname = variables.outputname
else:
    outputname = os.path.splitext(os.path.basename(fontname))[0]

output_fullpath = os.path.join(folder, outputname)

# ensure ending with .ufo
if not output_fullpath.endswith(".ufo"):
    output_fullpath += ".ufo"

if variables.zip:
    # add z for ufoz
    output_fullpath += "z"
else:
    # create folder if ufo folder not exist
    if not os.path.isdir(output_fullpath):
        os.makedirs(output_fullpath)

print("Starting conversion…")

#save ufo
ufo = defcon.Font()
extractor.extractUFO(fontname, ufo)
ufo.save(output_fullpath, structure=structure)

print("Conversion complete. UFO font at: " + output_fullpath)