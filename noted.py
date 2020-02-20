#!/usr/bin/python3

import click
from terminaltables import AsciiTable
from tagmodule import tagdb, new_item
import os
import glob

# Utility to get the correct notes dir from a config file. This can be improved to support a proper config file!
def get_notes_dir_from_config(config_file=None):
    if config_file:
        with open(os.path.expanduser(config_file), 'r') as config:
            config_lines = config.readlines()
            for line in config_lines:
                if 'outdir' in line:
                    basedir = os.path.expanduser(line.split('=')[1].strip())
                    return basedir
                basedir = os.path.expanduser('~/notes')
    else:
        basedir = os.path.expanduser('~/notes')
    return basedir


config_file = '~/tagdb.conf'
notes_dir = get_notes_dir_from_config(config_file)

# Get the categories for Click's tab completion with the new item option. Ignore the tmp dir.
def category_options(ctx, args, incomplete):
    category_list = []
    for category_dir in os.walk(notes_dir):
        if category_dir[0].strip('/') != 'tmp':
            category_list.append(category_dir[0].replace(notes_dir, '').strip('/'))
    return [k for k in category_list if incomplete in k]

def tag_options(ctx, args, incomplete):
    tag_list = []
    db = tagdb.db(notes_dir)
    all_tags = db.get_all_tags()
    for tag in all_tags:
        tag_list.append(tag['name'])
    return [k for k in tag_list if incomplete in k]

# Tag Notes Database CLI Options etc.
@click.group()
def cli():
    pass

@cli.command()
@click.option('-t', '--tags', multiple=True, type=click.STRING, autocompletion=tag_options, help='Search for items with tags.', )
@click.option('-o', '--output', help='output path for directory to be created')
def search(tags, output):
    """ Searches database for given tags """
    db = tagdb.db(notes_dir)
    items = db.get_items_with_tags(tags)
    if not items:
        click.echo('[-] No items found with those tags.')
        exit()

    all_items = [['title', 'category', 'file']]
    for item in items:
        details_list = []
        for key, info in item.items():
            details_list.append(info)
        all_items.append(details_list)                
    print(AsciiTable(all_items).table)

@cli.command()
def delete_database():
    """ Deletes the current database. Just like that. """
    os.remove(notes_dir + '/noted.db')
    print('Database deleted.')

@cli.command()
@click.option('-i', '--id', help='ID of the item to read.', required=True)
def view_item(id):
    """ View item with a given ID. """
    db = tagdb.db(notes_dir)
    print(db.get_item_titles())
    return db.get_item_titles()

@cli.command()
@click.option('-d', '--directory', help='Directory to import.', required=True, type=click.Path(exists=True))
def parse_dir(directory):
    """ Import directory of files into database. WARNING - If the files do not correspond to the template, this will break. """
    db = tagdb.db(notes_dir)
    print('[+] Getting all files. If using a network share this could take a while.')
    files = glob.glob(directory + '/**/*.md', recursive=True)
    for file in files:
        if not db.does_file_exist(file):
            print('[+] Parsing', file, 'to database')
            add_new_item = new_item.new_item(None, notes_dir)
            parsed_template_dict = add_new_item.parse_template(file)
            db.add_item(parsed_template_dict)
        else:
            print('[+]', file, 'already exists in database.')
    


@cli.command()
def view_all_items():
    """ View all items currently in the database. """
    header = ['ID', 'Title']
    db = tagdb.db(notes_dir)
    item_list = [header]
    for item_details in db.get_item_titles():
        single_item_list = []
        for key, item in item_details.items():
            single_item_list.append(item)
        item_list.append(single_item_list)
    table = AsciiTable(item_list)
    print(table.table)

@cli.command()
@click.option('-i', '--ids', required=True, help='Comma delimited list of IDs of the item to read.')
def view_items(ids):
    """ View a collection of items by their IDs. """
    id_list = ids.split(',')
    db = tagdb.db(notes_dir)
    print(db.get_item_titles())

@cli.command()
def view_tags():
    """ View all tags currently in the database. """
    db = tagdb.db(notes_dir)
    print(db.get_all_tags())


@cli.command()
@click.option('-c', '--category', type=click.STRING, autocompletion=category_options, required=False, help='Category to add the item to.')
@click.option('-T', '--title', required=False, help='Title of the note.')
@click.option('-t', '--tags', required=False, help='Comma delimited list of tags to add.')
def add_item(category, title, tags):
    """ Add a new item to the methodology """
    passthrough_dict = {'category': category, 'title': title, 'tags': tags}
    db = tagdb.db(notes_dir)
    add_item_to_db = new_item.new_item(passthrough_dict, notes_dir)
    item_to_add = add_item_to_db.get_user_input()
    db.add_item(item_to_add)
           


