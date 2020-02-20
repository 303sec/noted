#!/usr/bin/python3
# add-tag script

import os
import argparse
import shutil

class new_item:
	def __init__(self, category=None, outpath=None):
		if category != None:
			self.category = category
		if outpath == None:
			self.outpath = os.path.expanduser('~/notes')
		else:
			self.outpath = os.path.expanduser(outpath)
		return

	def get_data_between_lines(self, infile, startline, endline):
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


	def get_user_input(self):
		print('getuserinput')
		template_file = self.outpath + '/tag_template.md'
		template_file_temp = self.outpath + '/tmp/tag_template.md.tmp'
		# output_dir = '/mnt/google_drive/Methodology/'
		output_dir = self.outpath
		shutil.copyfile(template_file, template_file_temp)

		os.system('vim ' + template_file)

		output_dict = {}

		f = open(template_file, 'r')

		# Get the category and the title from the file
		x = f.readlines()
		title = x[0].strip('#').strip()
		title_file = title.replace(' ', '_') + '.md'
		print(title_file)
		if title_file == 'Item_Title.md':
			print('Failed. Idea Title not changed.')
			exit()

		if self.category == None:
			category = self.get_data_between_lines(x, "# Category:", "# Tags:")
			if category == '':
				category = 'uncategorised'
			# Remove leading or ending slashes for consistency
			category = category.strip('/')

		category_dir = self.outpath + '/' + category
		os.mkdirs(category_dir)
		outfile = category_dir + '/' + title_file
		shutil.move(template_file_temp, outfile)



		output_dict['title'] = x[0].strip('#').strip()
		output_dict['details'] = self.get_data_between_lines(x, "# Details:", "# References:")
		output_dict['refs'] = [i.strip('*').strip() for i in self.get_data_between_lines(x, "# References:", "# Category:").split('\n')]
		output_dict['category'] = self.get_data_between_lines(x, "# Category:", "# Tags:")
		output_dict['tags'] = [i for i in self.get_data_between_lines(x, "# Tags:", "# Notes:").split(',')]
		output_dict['notes'] = self.get_data_between_lines(x, "# Notes:", "<eof>")

		return output_dict

# We need to hook this up to the SQLite database and then we're good!
# Also worth outputting the file into the methodology directory, maybe with the category as a folder.


# output_file = output_dir + title_file

# shutil.move(template_file_temp, output_file)

# print('Success! Wrote file: ' + title_file + ' to Ideas/Unsorted')

