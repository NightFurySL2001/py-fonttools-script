import os
from natsort import os_sorted

import argparse

#give arguments
parser = argparse.ArgumentParser(description='List the current directory similar to Windows Explorer sorting.')
parser.add_argument("-f", '--folder', metavar='folder_path', default=".",
                    help='path to folder, default to current directory')
parser.add_argument("-o", '--output', metavar='output_txt', default="file_list.txt",
                    help='file name for list of file in directory, default to file_list.txt')

# print(os_sorted(os.listdir()))
# The directory sorted like your file browser might show

#parse arguments
args = parser.parse_args()

#get windows sorted list
files = os_sorted(os.listdir(args.folder))
#open output file
output_file = open(args.output, "w", encoding="utf-8")
#write
output_file.write("\n".join(files))
