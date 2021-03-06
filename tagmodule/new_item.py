#!/usr/bin/python3
# add-tag script

import os
import argparse
import shutil
import time

class new_item:
    def __init__(self, passthru_dict, outpath=None):
        self.cli_args = passthru_dict
        if outpath == None:
            self.outpath = os.path.expanduser('~/notes/')
        else:
            self.outpath = os.path.expanduser(outpath)
        self.original_template = self.template = '''# Item Title

## Details:
<DETAILS>

## References:
* [ref](url)

## Category:
<CATEGORY>

## Tags:
<TAGS>

<eof>
        '''
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

    def parse_template(self, template_file_temp):
        print('[+] Parsing file...')
        # Open the temp_template and get the title from the file
        with open(template_file_temp, 'r+') as template_file_read:
            x = template_file_read.readlines()
            template_file_read.seek(0)
            
            if template_file_read.read().strip() == self.original_template.strip():
                print('Failed. No changes.')
                exit()
            title = x[0].strip('#').strip()
            title_file = title.replace(' ', '_') + '.md'
            if title_file == 'Item_Title.md':
                ts = str(int(time.time()))
                title_file = 'Unnamed_' + ts + '.md'
                print('Warning! Idea Title not changed from default. Saving as', title_file)

            # Get the Category from the file
            category = self.get_data_between_lines(x, "## Category:", "## Tags:")
            if category == '':
                category = 'uncategorised'
            # Remove leading or ending slashes for consistency
            category = category.strip('/')

            category_dir = self.outpath + category
            if not os.path.exists(category_dir):
                print('Note type directory does not exist. Creating', category_dir)
                os.makedirs(category_dir)
            outfile = category_dir + '/' + title_file
            shutil.move(template_file_temp, outfile)

        # To return and put in the database
        output_dict = {}
        output_dict['title'] = x[0].strip('#').strip()
        output_dict['details'] = self.get_data_between_lines(x, "## Details:", "## References:")
        output_dict['refs'] = [i.strip('*').strip() for i in self.get_data_between_lines(x, "## References:", "## Category:").split('\n')]
        output_dict['category'] = self.get_data_between_lines(x, "## Category:", "## Tags:")
        output_dict['tags'] = [i.strip() for i in self.get_data_between_lines(x, "## Tags:", "<eof>").split(',')]
        output_dict['notes'] = ''
        output_dict['savefile'] = outfile

        return output_dict


    def get_user_input(self):
        ts = str(int(time.time()))
        temp_dir = self.outpath + '/tmp/'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        template_file_temp = temp_dir + ts + '.md.tmp'
        output_dir = self.outpath
        
        if self.cli_args['category']:
            self.template = self.template.replace('<CATEGORY>', self.cli_args['category'])
            category_tags = '<TAGS>, ' + ','.join(self.cli_args['category'].split('/'))
            self.template = self.template.replace('<TAGS>', category_tags)
        if self.cli_args['title']:
            self.template = self.template.replace('Item Title', self.cli_args['title'])
        if self.cli_args['tags']:
            self.template = self.template.replace('<TAGS>', self.cli_args['tags'])
        if self.cli_args['resources']:
            self.template = self.template.replace('* [ref](url)', self.cli_args['resources'])
        if self.cli_args['details']:
            self.template = self.template.replace('<DETAILS>', self.cli_args['details'])

        with open(template_file_temp, 'w+') as template_file_gen:
            template_file_gen.write(self.template)
            template_file_gen.close()

        if os.getenv('EDITOR'):
            editor = os.getenv('EDITOR')
            os.system(editor + ' ' + template_file_temp)
        else:
            os.system('vim ' + template_file_temp)

        output_dict = self.parse_template(template_file_temp)
        print(output_dict)
        return output_dict


