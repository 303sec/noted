To Do

19-02-2020

* [x] Allow selection of working directory and add default directory (Use a config file!)
* [x] Add savefile and category tags to database items
* [x] Add savefile and category to all database calls to get or edititems
* [x] Add functionality to add command line stuff to the template file as required.
* [x] Add CLI arguments such as category
* [x] Implement appropriate saving - with the root dir, create the directories specified by the category bit and name the file appropriately.
* [x] Implement category tab complete, look into python tab completion
* [x] Add the category (separated by /) to the template's tags 
	* [x] Test it works
* [x] Parse template files that are not in the database

__Output Stuff__
* [x] Get multiple tags as input from CLI
	* [x] BUG - Remove whitespace & make tags lowercase
	* [x] Test the bug is fixed
* [x] Fix the terrible tag input search
* [x] Search without output = list titles with categories, tags and filenames
* [x] Create outputs for tag scans - folder with symlinks to all the relevant files 


05-03-2020

__Features__

* [ ] When creating a md file, make a hash to check if the file has changed.
	* This should make it possible to edit any .md file and reparse the contents when changed.
* [ ] Different templates, for things such as simple resources. I don't want to have to write full articles on everything, as sometimes there are just really good resources with lots of info.
	* This could be a similar (but different) tool, used to aggregate URLs for study and research

30-05-2020

* [x] Add this todo list to todoist
* [ ] Clean up the click interface:	
	* view-all-items is missing some stuff
	* view-item doesn't return pleasant-looking information (and also doesn't work)
* [ ] BUG - the directory is stored from the machine being used, which makes no sense with the share.
	* search should also give the tags of the item
	* 
* [ ] Allow for 'resources' to be added with add-resource