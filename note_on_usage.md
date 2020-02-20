### Add item process
0. Find useful resource / discover technique
1. Run add-item command 
	* can include flags such as title, category (which should have auto complete) & tags
2. Creates a temporary markdown file used for editing containing any data included from flags
3. Once markdown file is saved, moves it to the relevant area in methodology/category/xxx
	* Note that the tags should also be auto-generated from the category (like tag=webapp, tag=injection, etc.)
	* Tagging practice is a bigger topic than to be discussed here, but generally things like 'technique', 'resource' and 'research' should be used in order to help get the right kind of details
4. Save the name & location of the file & details in the database. Note that the database details probably won't be used, but will be stored anyway because fuck it.

### Getting items by tag
0. Run the command get-items (or something) with flags equalling category and/or tag details. Also flag for output dir.
1. Create a text / markdown file with filenames & links to all items that have the searched tags
2. Alternatively, create a directory with symlinks to all the given tag
3. If we're trying to make a dynamic methodology, it could be worth creating a checklist from the created tags

### Future features
* Ability to edit items
	* Just as simple as putting in the name/ID of the item, opening the saved markdown file which was originally used, and then re-parsing that into the database (deleting original entry). Shouldn't actually be that difficult to implement.
* Web interface - a Markdown->HTML generator run against the methodology directory, and a page that shows all the titles for tags that have been searched for
* __Methodology/checklist builder__: Get each of the items from the database that have the relevant tags and create a markdown checklist. 
	* This is most effective if the tag system is working on a system-by-system basis - that is, we create tags for different pieces of software and versions of that software
	* An example of that would be an SQLite time based Injection item. This would have the tags sqli, sqlite, time based sqli
	* Note that an easy way to implement this for now would be to create a markdown file with all the file titles and [ ] when generating a directory / list of resources from a search.
* This is generally just a really useful system for taking notes. Regardless of the methodology stuff, having a damn simple category and tag system with a variety of note entry and retrival is pretty cool. Potentially having the ability to select 'notebooks' would be really useful, which just changes the working directory.