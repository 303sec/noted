#!/usr/bin/python3

# Script to Test various aspects of tagdb

import tagdb

print('creating db')
db = tagdb.db('./')

item_dict = {'title': 'test_title', 'details': 'I am describing this test object.', 'category': 'technology', 'refs':['http://google.com', 'https://anotherurl.com'], 'notes':None, 'tags':['one','two','thurmantastat']}

print('adding item')
db.add_item(item_dict)

# Above code works to insert data into the tag database


print('tag = one')
print(db.get_items_with_tags(['one']))


print('tags = one, two')
print(db.get_items_with_tags(['one', 'two']))
