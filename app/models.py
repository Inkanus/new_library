from datetime import datetime
from app import db

class Book(db.Model):
    __tablename__ = "Book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    description = db.Column(db.String(1000))
    publication_date = db.Column(db.DateTime)
    pages = db.Column(db.Integer, index=True)
    genres = db.Column(db.String(100))

    DEFAULTS = [
        "title",
        "author",
        "year",
        "genres",
        "pages",
        "description"
    ]

    def formatted(self):
        return {
            "id": self.id,
            "title": self.title,
            "authors": [
                f"{w.author_rel.name} {w.author_rel.surname}"
                for w in WrittenBy.query.filter_by(book_id=self.id).all()
            ],
            "description": self.description,
            "pages": self.pages,
            "year": datetime.strftime(self.publication_date, "%Y"),
            "genres": self.genres.split("-")
        }

class Author(db.Model):
    __tablename__ = "Author"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    surname = db.Column(db.String(100), index=True)
    birth = db.Column(db.DateTime)

class WrittenBy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('Author.id'))
    book_rel = db.relationship(
        "Book", backref=db.backref("book", uselist=False))
    author_rel = db.relationship(
        "Author", backref=db.backref("author", uselist=False))

class Rentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.id'))
    book_rel = db.relationship(
        "Book", backref=db.backref("book_rent", uselist=False))
    rented_at = db.Column(db.DateTime, default=datetime.utcnow)
    returned = db.Column(db.Boolean, default=False)

class Library:
    SORT_KEYS = {
        "id": Book.id,
        "title": Book.title,
        "year": Book.publication_date,
        "pages": Book.pages,
        "asc": db.asc,
        "desc": db.desc
    }

    @staticmethod
    def get_books(sort_key, sort_order):
        key = Library.SORT_KEYS[sort_key]
        order = Library.SORT_KEYS[sort_order]
        return [
            book.formatted() for book in Book.query.order_by(order(key)).all()
        ]

    @staticmethod
    def get_book(id, formatted=True):
        book = Book.query.get(id)
        if book and formatted:
            return book.formatted()
        return book

    @staticmethod
    def rent_book(id):
        rent = Rentals(book_id=id)
        db.session.add(rent)
        db.session.commit()
    
    @staticmethod
    def return_book(id):
        rental = Rentals.query.filter_by(
            book_id=id).order_by(db.desc(Rentals.rented_at)).first()
        rental.returned = True
        db.session.commit()

    @staticmethod
    def get_book_last_rent_time(id):
        last_rent = Rentals.query.filter_by(
            book_id=id).order_by(db.desc(Rentals.rented_at)).first()
        if last_rent:
            if not last_rent.returned:
                return datetime.strftime(last_rent.rented_at, "%d/%m/%y")
        return None

    @staticmethod
    def add_author(name, surname):
        auth = Author(
            name=name.capitalize(),
            surname=surname.capitalize()
        )
        db.session.add(auth)
        db.session.commit()
        return auth

    @staticmethod
    def handle_authors(data, book_id, from_api=False):
        if from_api:
            authors = data["authors"]
        else:
            authors = [data["authors-%d" % d] for d in range(3)]
        for author in authors:
            if author == "" or author is None:
                continue
            namesplit = author.split(" ")
            surname = namesplit[-1]
            name = " ".join(namesplit[:-1])
            auth = Author.query.filter(
                Author.name.like(name), Author.surname.like(surname)).first()
            if not auth:
                auth = Library.add_author(name, surname)
            Library.add_book_auth_rel(book_id, auth.id)

    @staticmethod
    def add_book_auth_rel(book_id, author_id):
        writtenby = WrittenBy(
                book_id=book_id,
                author_id=author_id
            )
        db.session.add(writtenby)
        db.session.commit()

    @staticmethod
    def parse_form_data(data, from_api=False):
        if from_api:
            genres = "-".join(data["genres"])
        else:
            genres = "-".join(
                [data["genres-%d" % d] for d in range(3)]
            ).strip()
        return {
            "title": data["title"],
            "publication_date": datetime.strptime(str(data["year"]), "%Y"),
            "pages": int(data["pages"]),
            "description": data.get("description", ""),
            "genres": genres
        }

    @staticmethod
    def add_book(data, from_api=False):
        parsed_data = Library.parse_form_data(data, from_api)
        book = Book(**parsed_data)
        db.session.add(book)
        db.session.commit()

        Library.handle_authors(data, book.id, from_api)
             
        return book.id
    
    @staticmethod
    def update_book(id, data, from_api=False):
        book = Library.get_book(id, formatted=False)
        parsed_data = Library.parse_form_data(data, from_api)
        book.title = parsed_data["title"]
        book.publication_date = parsed_data["publication_date"]
        book.genres = parsed_data["genres"]
        book.pages = parsed_data["pages"]
        book.description = parsed_data["description"]

        for rel in WrittenBy.query.filter_by(book_id=book.id):
            db.session.delete(rel)
            db.session.commit()

        Library.handle_authors(data, book.id, from_api)

        return book

    @staticmethod
    def delete_book(id):
        book = Library.get_book(id, formatted=False)
        db.session.delete(book)
        db.session.commit()
        for rel in WrittenBy.query.filter_by(book_id=id):
            db.session.delete(rel)
            db.session.commit()