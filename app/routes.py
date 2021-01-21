from flask import Flask, Blueprint, render_template, redirect, abort, request

from app import models, forms

routes = Blueprint('routes', __name__)

library = models.Library

@routes.route("/")
def index():
    return render_template("index.html")
    
@routes.route("/books")
@routes.route("/books/<int:id>")
def books(id=None):
    if id is not None:
        book = library.get_book(id)
        if not book:
            abort(404)
        rent_data = library.get_book_last_rent_time(id)
        return render_template("book.html", book=book, rent_data=rent_data)
    else:
        sort = request.args
        if not sort:
            return redirect("/books?sort_key=id&sort_order=asc")
        books = library.get_books(**sort)
        return render_template("books.html", books=books, args=sort)

@routes.route("/books/<int:id>/rent")
def rent_book(id):
    library.rent_book(id)
    return redirect("/books/%d" % id)

@routes.route("/books/<int:id>/return")
def return_book(id):
    library.return_book(id)
    return redirect("/books/%d" % id)

@routes.route("/edit_book/", methods=["GET", "POST"])
@routes.route("/edit_book/<id>", methods=["GET", "POST"])
def edit_book(id=None):
    form = forms.EditBook()
    if request.method == "GET":
        book = None
        if id is not None:
            book = library.get_book(int(id))
            if not book:
                abort(404)
        form = form.load_data(book)
        return render_template(
            "editbook.html", book=book,
            form=form, error=None)
    else:
        if form.validate_on_submit():
            if id is None:
                id = library.add_book(request.form)
            else:
                library.update_book(int(id), request.form)
            return redirect("/books/%d" % int(id))
        else:
            book = None
            error = form.errors
            return render_template(
                "editbook.html", book=book,
                form=form, error=error)

@routes.route("/delete_book/<int:id>")
def delete_book(id):
    library.delete_book(id)
    return redirect("/books")
