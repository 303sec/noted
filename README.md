# noted

A tool to help meticulously organise notes. I use it for keeping track of my pentesting methodology and security research.

## Installation

```
git clone https://github.com/303sec/noted
cd noted
pip install -r requirements.txt
```

## Usage

`noted add-item`
Opens the text editor specified by the $EDITOR environment variable (default: vim), with the template to add an item to the configured note directory.
Saving the file creates a markdown file with the title of the issue in the given category directory.

`noted add-item -T 'Title' -t tag_one,tag_two -c base_category/one_level_in_category`
Opens the text editor (as above), which will open with pre-populated title, tags and category.

