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

parser.add_argument('fontname', type=check_font)
parser.add_argument('-f', '--folder')
parser.add_argument('-o', '--outputname')

if sys.argv[0].endswith((".py",".exe")):
    sys.argv.pop(0) #remove current running script from list of args

variables = parser.parse_args(sys.argv)

#font name as parameter 1
#fontname = sys.argv[1]
fontname = variables.fontname

#folder name as parameter 2
#if len(sys.argv) > 2:
if variables.folder is not None:
    #folder = sys.argv[2]
    folder = variables.folder
    if not folder.endswith(("/","\\")):
        folder+="/"
else:
    folder = "./"

#if folder not exist
if not os.path.isdir(folder):
    os.mkdir(folder)

#check output font name
if variables.outputname is not None:
    outputname = variables.outputname
else:
    outputname = fontname[:-4]+".ufo"

print("Starting conversion…")

#save ufo
ufo = defcon.Font()
extractor.extractUFO(fontname, ufo)
ufo.save(folder+outputname)

print("Conversion complete. UFO font at: " + folder+outputname)