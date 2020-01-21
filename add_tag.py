 #!/usr/bin/python3
# add-tag script

import os
import argparse
import shutil


def get_data_between_lines(infile, startline, endline):
	outlist = []
	copy = False
	for line in infile:
	    if line.strip() == startline:
	        copy = True
	        continue
	    elif line.strip() == endline:
	        copy = False
	        continue
	    elif copy:
	        outlist.append(line)
	return ''.join(outlist).strip()



template_file = '/mnt/google_drive/Methodology/tag_template.md'
template_file_temp = '/tmp/tag_template.md.tmp'
output_dir = '/mnt/google_drive/Methodology/'
shutil.copyfile(template_file, template_file_temp)

os.system('vim ' + template_file)

output_dict = {}

f = open(template_file, 'r')
x = f.readlines()
title = x[0].strip('#').strip()
title_file = title.replace(' ', '_') + '.md'
if title_file == 'Item_Title.md':
	print('Failed. Idea Title not changed.')
	exit()

output_dict['title'] = x[0].strip('#').strip()
output_dict['details'] = get_data_between_lines(x, "# Details:", "# References:")
output_dict['references'] = get_data_between_lines(x, "# References:", "# Category:")
output_dict['category'] = get_data_between_lines(x, "# Category:", "# Tags:")
output_dict['tags'] = get_data_between_lines(x, "# Tags:", "# Notes:")
output_dict['notes'] = get_data_between_lines(x, "# Notes:", "<eof>")

print(output_dict)

# We need to hook this up to the SQLite database and then we're good!
# Also worth outputting the file into the methodology directory, maybe with the category as a folder.


# output_file = output_dir + title_file

# shutil.move(template_file_temp, output_file)

# print('Success! Wrote file: ' + title_file + ' to Ideas/Unsorted')

