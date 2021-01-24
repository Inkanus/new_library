import json


class Book:
    DEFAULTS = {
        "title": "",
        "author": "",
        "year": 0,
        "genres": [""] * 3,
        "pages": 0,
        "description": ""
    }


def __init__(self, id, title, author, year, genres, pages, description):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.genres = genres
        self.pages = pages
        self.description = description

    @classmethod
    def as_blank(cls):
        return cls(*[None] * 4, [None] * 3, *[None] * 2)

    @classmethod
    def from_dict(cls, id, object, from_request=False):
        if from_request:
            genres = []
            for i in range(len(
                [k for k in object.keys() if k.startswith('genres')]
            )):
                genres.append(object["genres-%d" % i])
        else:
            genres = object["genres"]
        return cls(
            id,
            object["title"],
            object["author"],
            int(object["year"]),
            genres,
            int(object["pages"]),
            object["description"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genres": self.genres,
            "pages": self.pages,
            "description": self.description
        }

class Library:
    FILEPATH = ""
    SORT_KEYS = {
        "id": lambda x: x.id,
        "title": lambda x: x.title,
        "author": lambda x: x.author,
        "year": lambda x: x.year,
        "pages": lambda x: x.pages,
        "asc": False,
        "desc": True
    }
    def __init__(self, books=None):
        if books:
            self.books = books
        else:
            self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, id):
        for book in self.books:
            if book.id == id:
                self.books.remove(book)
                return True

    def update_book(self, id, book):
        self.remove_book(id)
        self.add_book(book)

    def get_book(self, id):
        for book in self.books:
            if book.id == id:
                return book

    def get_books(self, sort_key="id", sort_order="asc"):
        key = self.SORT_KEYS[sort_key]
        reverse = self.SORT_KEYS[sort_order]
        return sorted(self.books, key=key, reverse=reverse)

    def reorder(self):
        for i, book in enumerate(self.get_books("id")):
            book.id = i

    @classmethod
    def from_json(cls, filepath):
        try:
            with open(filepath) as obj:
                data = json.load(obj)
        except Exception as e:
            print("Error - ", e)
            return cls()

        books = []
        for item in data:
            id = item.pop('id')
            book = Book.from_dict(id, item)
            books.append(book)
        
        return cls(books)

    def to_json(self, books):
        return [book.to_dict() for book in books]

    @staticmethod
    def str_to_json(data):
        try:
            return json.loads(data)
        except:
            return None

    def save(self):
        try:
            with open(self.FILEPATH, "w") as obj:
                books = self.to_json(self.books)
                json.dump(books, obj)
        except Exception as e:
            print("Error - ", e)
