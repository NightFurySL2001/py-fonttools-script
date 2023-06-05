## Author: NightFurySL2001 (https://github.com/NightFurySL2001/py-fonttools-script)
## Copyright © 2022 NightFurySL2001 (NFSL2001)
## Released under MIT License

from itertools import chain
import sys
import os.path

from fontTools.ttLib import TTFont, TTCollection
from fontTools.unicode import Unicode


try:
    input_file=sys.argv[1]
except:
    while True:
        user_input_file = input("输入文件（相对或绝对）路径；按Enter以退出：")
        if user_input_file == "":
            print("无字体。")
            input("按Enter以退出。")
            sys.exit(0)
        elif os.path.isfile(user_input_file):
            input_file = user_input_file
            break
        else:
            print("字体不存在。")
            continue

### FUNC get TTC names
def get_ttc_list(filename):
    #clear font list
    ttc_names = []
    #lazy=True: https://github.com/fonttools/fonttools/issues/2019
    ttc = TTCollection(filename, lazy=True)
    for font in ttc:
        # single font name in getName(nameID, platformID, platEncID, langID=None), 0x409 make sure all font in English name
        ttf_name=font["name"].getName(4, 3, 1, 0x409)
        # add the font name itself instead of the XML representation
        ttc_names.append(str(ttf_name))
    #return array of names
    return ttc_names
### END

try: # normal single font
    ttf = TTFont(input_file, 0, allowVID=0,
                    ignoreDecompileErrors=True,
                    fontNumber=-1)
except: # ask for ttc
    font_names = get_ttc_list(input_file)
    for index, name in enumerate(font_names): #get a list of font names and display for choice
        print(str(index) + ". " + name)
    while True:
        font_no = int(input("Please choose a font file to count: "))
        if font_no >= 0 and font_no < len(font_names):
            ttf = TTFont(input_file, 0, allowVID=0,
                        ignoreDecompileErrors=True,
                        fontNumber=font_no)
            break
        

print("导出中……请勿关闭。")

chars = chain.from_iterable([y for y in x.cmap.items()] for x in ttf["cmap"].tables)
#print(list(chars))

###FUNC DEF START

#conversion to base 10, return 0 if failed
def deci(number):
    try:
        return int(number,16)
    except:
        return 0

# special check range function as python default range don't include ending number
def char_range(start, end):
    return range(start, end+1)
# normal range: range(0,5) --> [0,1,2,3,4], len(range(0,5))=5
# character detect range: char_range(0,5) --> [0,1,2,3,4,5], len(char_range(0,5))=6

#check range of character:
def uni_range_check(char_base10):
    #filter and count unicode
    if char_base10 in char_range(deci("4E00"), deci("9FFF")): #4E00 - 9FFF CJK Unified Ideographs
        return "basic"
    elif char_base10 in char_range(deci("2F00"), deci("2FDF")): #2F00 — 2FDF Kangxi Radicals
        return "kangxi"
    elif char_base10 in char_range(deci("2E80"), deci("2EFF")): #2E80 — 2EFF CJK Radical Supplements
        return "kangxi-sup"
    elif char_base10 == 12295: # U+3007 Ideographic Number Zero Unicode Character
        return "zero"
    elif char_base10 in char_range(deci("3400"), deci("4DBF")): #3400 — 4DBF CJK Unified Ideographs Extension A
        return "ext-a"
    elif char_base10 in char_range(deci("F900"), deci("FAFF")): #F900 — FAFF CJK Compatibility Ideographs
        return "compat"
    elif char_base10 in char_range(deci("20000"), deci("2A6DF")): #20000 — 2A6DF CJK Unified Ideographs Extension B
        return "ext-b"
    elif char_base10 in char_range(deci("2A700"), deci("2B73F")): #2A700 – 2B73F CJK Unified Ideographs Extension C
        return "ext-c"
    elif char_base10 in char_range(deci("2B740"), deci("2B81F")): #2B740 – 2B81F CJK Unified Ideographs Extension D
        return "ext-d"
    elif char_base10 in char_range(deci("2B820"), deci("2CEAF")): #2B820 – 2CEAF CJK Unified Ideographs Extension E
        return "ext-e"
    elif char_base10 in char_range(deci("2CEB0"), deci("2EBEF")): #2CEB0 – 2EBEF CJK Unified Ideographs Extension F
        return "ext-f"
    elif char_base10 in char_range(deci("2F800"), deci("2FA1F")): #2F800 — 2FA1F CJK Compatibility Ideographs Supplement
        return "compat-sup"
    elif char_base10 in char_range(deci("30000"), deci("3134F")): #30000 - 3134F CJK Unified Ideographs Extension G
        return "ext-g"
    elif char_base10 in char_range(deci("31350"), deci("323AF")): #31350 - 323AF CJK Unified Ideographs Extension H
        return "ext-h"
    return None
    
###FUNC DEF END

cjk_char_count = 0
outfile = open(input_file+"-han.txt", 'w', encoding='utf-8')
lines_seen = []
for line in chars:
    if line[0] in lines_seen:
        continue
    if uni_range_check(line[0]):
        outfile.write(chr(line[0])+"\n")
        cjk_char_count+=1
    lines_seen.append(line[0])

#finish count close font
ttf.close()

print("已完成。总汉字数："+str(cjk_char_count))
print("导出文件名："+str(input_file)+"-han.txt")
input("按Enter以退出。")
# strip() only remove \n, \r is left in string
