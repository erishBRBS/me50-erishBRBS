# CS50W Project 1: Wiki

This is my submission for CS50W Project 1: Wiki.

## Description

This project is a Wikipedia-like online encyclopedia built with Django. Users can view encyclopedia entries, search entries, create new pages, edit existing pages, and open a random entry.

## Features

- View encyclopedia entries
- Search for entries
- Display search results for partial matches
- Create new encyclopedia pages
- Edit existing encyclopedia pages
- Open a random encyclopedia page
- Convert Markdown content to HTML

## Files

- `manage.py` - Django project management script
- `wiki/` - Main Django project folder
  - `settings.py` - Django settings
  - `urls.py` - Main URL configuration
- `encyclopedia/` - Main app folder
  - `views.py` - Contains the view functions for index, entry, search, new page, edit page, and random page
  - `urls.py` - App URL routes
  - `util.py` - Helper functions for reading and saving entries
  - `forms.py` - Django forms used for creating and editing entries
  - `templates/encyclopedia/` - HTML templates
  - `static/encyclopedia/styles.css` - CSS styling
- `entries/` - Markdown files for encyclopedia entries

## Demo Checklist
- User can view a list of all encyclopedia entries on the index page
- User can click an entry title to view the full encyclopedia entry page
- User can search for an exact entry title and be redirected to that entry page
- User can search for a partial title and see matching search results
- User can create a new encyclopedia entry
- User cannot create a duplicate entry with the same title
- User can edit an existing encyclopedia entry
- User can open a random encyclopedia entry
- Markdown content is converted to HTML before being displayed
- Invalid or missing pages show an error page