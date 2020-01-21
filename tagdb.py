#!/bin/python3

import sqlite3
import os
import time


# http://howto.philippkeller.com/2005/04/24/Tags-Database-schemas/
# 'Toxi' solution

'''
Intersection (AND)

Query for bookmark+webservice+semweb

SELECT b.*
FROM tagmap bt, bookmark b, tag t
WHERE bt.tag_id = t.tag_id
AND (t.name IN ('bookmark', 'webservice', 'semweb'))
AND b.id = bt.bookmark_id
GROUP BY b.id
HAVING COUNT( b.id )=3

Union (OR)

Query for bookmark|webservice|semweb

SELECT b.*
FROM tagmap bt, bookmark b, tag t
WHERE bt.tag_id = t.tag_id
AND (t.name IN ('bookmark', 'webservice', 'semweb'))
AND b.id = bt.bookmark_id
GROUP BY b.id

'''


'''
CREATE TABLE info (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    details TEXT NOT NULL,
    refs TEXT,
    time_created DATE NOT NULL    
    )
CREATE TABLE tagmap (
    id INTEGER PRIMARY KEY,
    bookmark_id INTEGER,
    tag_id INTEGER
    )
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT
    )

'''

'''
item dict input format:

{
    'title': '',
    'details': '',
    'category': '',
    'references': [],
    'notes': '',
    'tags': [],
}
If the item is not included, it needs to be passed through as None.


{'title': 'test_title', 'details': 'I am describing this test object.', 'category': 'technology', 'references':['http://google.com', 'https://anotherurl.com'], 'notes':None, 'tags':['one','two','thurmantastat']}

'''

class db:
    def __init__(self, base_dir):
        self.db_name = base_dir + '/tags.db'
        
        if not os.path.exists(self.db_name):
            print('[+] Creating database at', self.db_name)

        connection = sqlite3.connect(self.db_name)
        cursor= connection.cursor();
        # Create the info table
        try:
            cursor.execute('''CREATE TABLE info (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                details TEXT NOT NULL,
                refs TEXT,
                notes TEXT,
                file TEXT,
                time_created DATE NOT NULL        
            )''')
            print('[+] Created table info')
        except Exception as e:
            pass
        # Create the tagmap
        try:
            cursor.execute('''CREATE TABLE tagmap (
                id INTEGER PRIMARY KEY,
                item_id INTEGER,
                tag_id INTEGER
            )''')
            print('[+] Created table tagmap')
        except Exception as e:
            pass

        try:
            cursor.execute('''CREATE TABLE tags (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT
                )''')
            print('[+] Created table tags')
        except Exception as e:
            pass


    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def add_tag(self, tag, category=None):
        connection = sqlite3.connect(self.db_name)
        cursor= connection.cursor();
        # Should add given information into the database.
        if category:
            cursor.execute('INSERT INTO tags (name, category) VALUES (?, ?)',(tag, category))
            connection.commit() 
            connection.close()
            return 0
        else:
            cursor.execute('INSERT INTO tags (name) VALUES (?)',(tag,))
            connection.commit() 
            connection.close()
            return 0


    def add_item(self, item_dict):
        if not 'title' in item_dict and not 'details' in item_dict:
            return (-1, 'Title and Details required in item_dict') 
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        for tag in item_dict['tags']:
            tag = tag.lower()
            if not self.does_tag_exist(tag):
                # New tag - let's create it!
                print('[+] Creating new tag:', tag)
                cursor.execute('INSERT INTO tags (name) VALUES (?)',(tag,))
                connection.commit() 
        ts = int(time.time())
        # Check that the minimum requirements of title and details are included
        cursor.execute('INSERT INTO info (title, details, refs, time_created) VALUES (?, ?, ?, ?)',(item_dict['title'], item_dict['details'], ','.join(item_dict['refs']), ts))
        item_id = cursor.lastrowid
        connection.commit()
        for tag in item_dict['tags']:
            tag = tag.lower()
            cursor.execute('SELECT id FROM tags where name = ?', (tag,))
            tag_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO tagmap (item_id, tag_id) VALUES (?, ?)', (item_id, tag_id))
            connection.commit()
        connection.close()

    # Assumes there's only one tag with that name - there should never be duplicates.
    def get_tag_id(self, tag):
        tag = tag.lower()
        tag_arr_return = []
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = sqlite3.Row
        cursor= connection.cursor();
        cursor.execute('SELECT id FROM tags WHERE name=?', (tag,))
        return cursor.fetchall()[0]

    def get_tag_ids(self, tag_arr):
        tag_arr_return = []
        for tag in tag_arr:
            tag = tag.lower()
            connection = sqlite3.connect(self.db_name)
            connection.row_factory = sqlite3.Row
            cursor= connection.cursor();
            cursor.execute('SELECT id, name FROM tags WHERE name=?', (tag,))
            tag_arr_return = append([dict(row) for row in cursor.fetchall()])
        return tag_arr_return

    def does_tag_exist(self, tag):
        tag = tag.lower()
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = sqlite3.Row
        cursor= connection.cursor();
        cursor.execute('SELECT * FROM tags WHERE name=?', (tag,))
        if cursor.fetchall():
            return True
        else:
            return False


    def get_items_with_tags(self, tag_arr):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self.dict_factory 
        cursor= connection.cursor()
        tag_amount = len(tag_arr)
        # Okay this is really bad.
        if tag_amount == 1:
            db_result=cursor.execute("SELECT * FROM tagmap, info, tags WHERE tagmap.tag_id = tags.id AND (tags.name IN (?)) AND info.id = tagmap.item_id GROUP BY info.id HAVING COUNT( info.id )=1", (tag_arr[0],))
        elif tag_amount == 2:
            db_result=cursor.execute("SELECT * FROM tagmap, info, tags WHERE tagmap.tag_id = tags.id AND (tags.name IN (?, ?)) AND info.id = tagmap.item_id GROUP BY info.id HAVING COUNT( info.id )=2", (tag_arr[0],tag_arr[1]))
        elif tag_amount == 3:
            db_result=cursor.execute("SELECT * FROM tagmap, info, tags WHERE tagmap.tag_id = tags.id AND (tags.name IN (?, ?, ?)) AND info.id = tagmap.item_id GROUP BY info.id HAVING COUNT( info.id )=3", (tag_arr[0],tag_arr[1],tag_arr[2]))
        elif tag_amount == 4:
            db_result=cursor.execute("SELECT * FROM tagmap, info, tags WHERE tagmap.tag_id = tags.id AND (tags.name IN (?, ?, ?, ?)) AND info.id = tagmap.item_id GROUP BY info.id HAVING COUNT( info.id )=4", (tag_arr[0],tag_arr[1],tag_arr[2],tag_arr[3]))
        elif tag_amount == 5:
            db_result=cursor.execute("SELECT * FROM tagmap, info, tags WHERE tagmap.tag_id = tags.id AND (tags.name IN (?, ?, ?, ?, ?)) AND info.id = tagmap.item_id GROUP BY info.id HAVING COUNT( info.id )=5", (tag_arr[0],tag_arr[1],tag_arr[2],tag_arr[3],tag_arr[4]))
        else:
            print('too many tags... only 5 supported because I\'m a bad dev.')
            return (-1, 'too many tags')
        return db_result.fetchall() 
        '''
        SQL query:
        SELECT * FROM tagmap, info, tags WHERE tagmap.tag_id = tags.id AND (tags.name IN ('two', 'one')) AND info.id = tagmap.item_id GROUP BY info.id HAVING COUNT( info.id )=2
        
        Immediate implementation quirk - going to have to figure out how to do tag lookups correctly. It might have to be as basic as if tags.length = 1, =2, etc. which is a shame but if it works it works!
        '''




'''
functions to create:

*[x] add_tag(tag, category=None)
    * return 0 for success
*[x] add_item(title, details, references)
    * return 0 for success
*[ ] add_tags_to_item(item_id, tag_arr)
    * return 0 for success
*[ ] add_tag_to_item(item_id, tag_name)
    * return 0 for success
*[ ] remove_tags_from_item(item_id, tag_name)
    * return 0 for success
*[ ] remove_item(item_id)
    * return 0 for success
*[ ] remove_tag(tag_name)
    * return 0 for success

*[ ] does_tag_exist(tag)
    * return bool
*[ ] get_similar_tags(tag_array)
    * return array of strings of similar tags

*[ ]get_items_with_tags()
    * return array of items with their full tag list

'''










