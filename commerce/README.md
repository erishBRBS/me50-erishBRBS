# CS50W Project 2 - Commerce

This is a complete Django implementation of the CS50W Commerce project: an eBay-like auction site.

## Features

- User registration, login, and logout
- Create auction listings
- View active listings
- View listing details
- Place valid bids
- Add/remove listings from watchlist
- Close auction as listing owner
- Winner message on closed auction
- Add and view comments
- Browse categories
- Manage listings, bids, comments, and categories through Django admin

## Setup

From inside the project folder:

```bash
python manage.py makemigrations auctions
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## Recommended categories to add in admin

- Fashion
- Electronics
- Toys
- Home
- Books
- Gaming

## Testing flow

1. Register User A.
2. Create a listing as User A.
3. Register User B.
4. Bid on User A's listing.
5. Add the listing to User B's watchlist.
6. Comment on the listing.
7. Log back in as User A.
8. Close the auction.
9. Log back in as User B and check the winner message.
