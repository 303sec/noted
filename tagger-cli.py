#!/usr/bin/python3

import click
from terminaltables import AsciiTable
from tagmodule import tagdb, add_item
import os

'''
table_data = [
['Heading1', 'Heading2'],
['row1 column1', 'row1 column2'],
['row2 column1', 'row2 column2']
        ]
table = AsciiTable(table_data)
'''

# Tag database CLI
@click.group()
def cli():
    pass

@cli.command()
@click.option('-t', '--tags', help='Search for items with tag by comma delimited tags.')
def search(tags):
    """ Searches database for given tags """
    tag_list = []
    for tag in tags.split(','):
        tag_list.append(tag)
    db = tagdb.db('./')
    items = db.get_items_with_tags(tag_list)
    if not items:
        click.echo('[-] No items found with those tags.')
        exit()
    for item in items:
        heading_list = ['title', 'details', 'notes','references']
        details_list = []
        #print(item)
        for detail in item:
                details_list.append(detail)
        printable_list = [heading_list, details_list]
        print(AsciiTable(printable_list).table)
           
@cli.command()
def delete_database():
    """ Deletes the current database. Just like that. """
    os.remove('./tags.db')

@cli.command()
@click.option('-i', '--id', help='ID of the item to read.', required=True)
def view_item(id):
    """ View item with a given ID. """
    db = tagdb.db('./')
    return db.get_item_titles()


@cli.command()
def view_all_items():
    """ View all items currently in the database. """
    db = tagdb.db('./')
    header = ['ID', 'Title']
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
    db = tagdb.db('./')
    print(db.get_item_titles())

@cli.command()
def view_tags():
    """ View all tags currently in the database. """
    db = tagdb.db('./')
    print(db.get_all_tags())

@cli.command()
def new_item():
    """ Add a new item to the methodology """
    add_item_to_db = add_item.add_item('./')
    db = tagdb.db('./')
    item_to_add = add_item_to_db.get_user_input()
    print(item_to_add)
    db.add_item(item_to_add)
           
if __name__ == '__main__':
        cli()

