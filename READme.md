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