# noted

A tool to help meticulously organise notes. I use it for keeping track of my pentesting methodology and security research.

## Installation

```
git clone https://github.com/303sec/noted
cd noted
pip install -r requirements.txt
```

## Usage

### Add Item

This adds an item to the methodology directory.

`noted add-item`

Opens the text editor specified by the $EDITOR environment variable (default: vim), with the template to add an item to the configured note directory.
Saving the file creates a markdown file with the title of the issue in the given category directory.

`noted add-item -T 'Title' -t tag_one,tag_two -c base_category/one_level_in_category`

Opens the text editor (as above), which will open with pre-populated title, tags and category.

### Add Idea

Adds an idea to the idea dir. Identical to add item except with the directory.

`noted add-idea`

### Add Bug Report

Adds a new bug report, exactly like add-item. 

`noted add-bugreport`

## Tag Guide

There will be a variety of tags that define documents in Noted, a definitive list of these tags is as follows:

* resource
* wordlist
* poc
* tool\_usage
* technique
* methodology
* quick\_tips

These formats reference the type of data stored in the file, and the following breakdown can give more insight into what to add .


#### Resource

A title & URL (or collection of URLS). No need for a description. 

#### Payload

Contains a section titled Payloads, with a collection of items to add to a wordlist used for the note's purposes.

#### Tool Usage

Contains a guide on aspects or a full overview of a tool. Basically a tool cheatsheet.
Try to break these down into different parts - so no just 'Hydra usage', but 'Hydra Web Authentication Usage'. If it's the basic overview of the tool, title it '{tool} Basic Usage'.

#### Technique

Details a specific technique for an attack. For example, bypassing a filter with unicode. The given technique should have a detailed technical breakdown.

#### Methodology

A methodology item. Essentially part of the root category's methodology, so with any notes tagged with this it'll be added to the methodology to follow on most/all tests.

#### PoC

Proof-of-concept: contains a code block with a proof of concept exploit.

#### Quick Tips

What is says on the tin: Just a quick one-liner or tip to remember a thing.
