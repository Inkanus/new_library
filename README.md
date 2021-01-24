# Home Library

Home Library is a flask-based website that lets you save your favorite books.

## Prerequisites

* Python 3.9+

## Installation

Clone the repo via Git
```
git clone https://github.com/..
```
Install packages required using pip
```
pip install -r requirements.txt
```

## Usage

Run the server
```
python home_library.py
```
Visit http://localhost:5000 using your browser, from there start adding books
using the dedicated form or view them in the My Books section, sorting as you prefer.
You can take a closer look to each book by clicking on their titles,
and also edit their labels or delete them completely.

## REST Api

Home Library is provided with a REST Api to get, create, edit and delete books in your
library using HTTP requests.

All of the examples provided are using python requests library.

### GET

Use GET requests to get all of the library data or a specified book's information.

```python
import requests

# Getting the full library
requests.get("http://localhost:5000/api/v1/books")

# Specify url parameters to get a sorted copy of library
params = {
    "sort_key": "title", # or "author", "year", "pages"
    "sort_order": "asc" # or "desc"}
# Passing them to the call to requests.get
requests.get("http://localhost:5000/api/v1/books", params=params)

# Getting data from a specific book
book_id = 0
requests.get("http://localhost:5000/api/v1/books/%d" % book_id)
```

### POST

Use POST requests to save new books into the library, send json data.

```python
import json
import requests

# "genres" and "description" are optional and can be not specified
data = {
    "title": "Eragon",
    "author": "Christopher Paolini",
    "year": 2002, 
    "genres": [
        "fantasy", "dystopian", "" # specify up to three genres, leave empty strings
    ],
    "pages": 509,
    "description": """
        Eragon is the first book in The Inheritance Cycle
        by American fantasy writer Christopher Paolini.
    """}
# Making the request passing json data
requests.post("http://localhost:5000/api/v1/books", json=json.dumps(data))
```

### DELETE

Use DELETE requests to remove books from the library.

```python
import requests

book_id = 0
requests.delete("http://localhost:5000/api/v1/books/%d" % book_id)
```

### PUT

Use PUT requests to update specific books in the library.

```python
import json
import requests

book_id = 0
data = {
    "author": "Christopher Paolini",
    "year": 2002}
requests.put(
    "http://localhost:5000/api/v1/books/%d" % book_id,
    json=json.dumps(data))
```