#!/usr/bin/python3

import click
from terminaltables import AsciiTable
from tagmodule import tagdb, add_item
import os


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

   		print(item)
   		# print(AsciiTable(item).table)
	   
@cli.command()
def delete_database():
    """ Deletes the current database. Just like that. """
    os.remove('./tags.db')

@cli.command()
def new_item():
    add_item_to_db = add_item.add_item('./')
    db = tagdb.db('./')
    item_to_add = add_item_to_db.get_user_input()
    print(item_to_add)
    db.add_item(item_to_add)
	   


if __name__ == '__main__':
	cli()

