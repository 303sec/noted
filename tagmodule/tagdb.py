#!/bin/python3

import sqlite3
import os
import time

class db:
    def __init__(self, base_dir):
        self.db_name = base_dir + 'noted.db'
        
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
                category TEXT NOT NULL,
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
            if not self.does_tag_exist(tag) and tag.strip() != '':
                # New tag - let's create it!
                print('[+] Creating new tag:', tag)
                cursor.execute('INSERT INTO tags (name) VALUES (?)',(tag.strip().lower(),))
                connection.commit() 
        ts = int(time.time())
        # Check that the minimum requirements of title and details are included
        cursor.execute('INSERT INTO info (title, details, category, refs, file, time_created) VALUES (?, ?, ?, ?, ?, ?)',(item_dict['title'].strip(), item_dict['details'].strip(), item_dict['category'].strip().lower(),','.join(item_dict['refs']), item_dict['savefile'], ts))
        item_id = cursor.lastrowid
        connection.commit()
        for tag in item_dict['tags']:
            if tag != '':
                tag = tag.lower()
                cursor.execute('SELECT id FROM tags where name = ?', (tag.strip().lower(),))
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
            connection.row_factory = self.dict_factory
            cursor= connection.cursor();
            cursor.execute('SELECT id, name FROM tags WHERE name=?', (tag,))
            tag_arr_return = append([dict(row) for row in cursor.fetchall()])
        return tag_arr_return

    def get_all_tags(self):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self.dict_factory
        cursor= connection.cursor();
        cursor.execute('SELECT name FROM tags')
        return cursor.fetchall()

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

    def does_file_exist(self, file):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = sqlite3.Row
        cursor= connection.cursor();
        cursor.execute('SELECT * FROM info WHERE file=?', (file,))
        if cursor.fetchall():
            return True
        else:
            return False

    def get_item_titles(self):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self.dict_factory
        cursor= connection.cursor();
        cursor.execute('SELECT id, title FROM info')
        return cursor.fetchall()


    def get_item_by_id(self, item_id):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self.dict_factory
        cursor= connection.cursor();
        cursor.execute('SELECT title, details, notes, refs FROM info where id=?', (item_id,))
        return cursor.fetchall()

    def get_items_with_tags(self, tag_arr):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self.dict_factory 
        cursor= connection.cursor()
        tag_amount = len(tag_arr)
        # Better than before, at least. Now creates (?,?) dependent on amount of tags given, which is concatented with the SQL query.
        if tag_amount == 1:
            tag_name_query_in = '(?)'
        else:
            tag_name_query_in = '('
            for tag in range(tag_amount):
                tag_name_query_in = tag_name_query_in + '?,'
            tag_name_query_in = tag_name_query_in[:-1] + ')'

        sql_query = "SELECT title, info.category, file FROM info, tagmap, tags WHERE tagmap.tag_id = tags.id AND (tags.name IN" + tag_name_query_in + ") AND info.id = tagmap.item_id GROUP BY info.id HAVING COUNT( info.id )=" + str(tag_amount)
        db_result=cursor.execute(sql_query, tag_arr)        
        return db_result.fetchall() 





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










