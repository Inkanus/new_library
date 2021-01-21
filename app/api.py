import json

from flask import Blueprint, request, jsonify, abort, make_response

from app import models, utils

apis = Blueprint('apis', __name__)

library = models.Library

@apis.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': 'Not found',
        'status_code': 404
    }), 404)

@apis.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({
        'error': 'Bad request',
        'status_code': 400
    }), 400)

@apis.route("/api/v1/books", methods=["GET"])
def api_list_books():
    args = request.args
    if not args:
        args = {"sort_key": "id", "sort_order": "asc"}
    if not utils.valid_get(args):
        abort(400)
    books = library.get_books(
        **dict(
            (k, args.get(k)) for k in args if k in ["sort_order", "sort_key"]
        )
    )
    return jsonify({
        "books": books,
        "sort_key": args.get("sort_key", "id"),
        "sort_order": args.get("sort_order", "asc"),
    })

@apis.route("/api/v1/books/<int:id>", methods=["GET"])
def api_get_book(id):
    book = library.get_book(id, False)
    if not book:
        abort(404)
    return jsonify({"book": book.formatted()})

@apis.route("/api/v1/books", methods=["POST"])
def api_new_book():
    data = json.loads(request.json)
    if not data or not utils.valid_post_put(data):
        abort(400)
    book_id = library.add_book(data, True)
    return jsonify({'book': library.get_book(book_id)}), 201

@apis.route("/api/v1/books/<int:id>", methods=["DELETE"])
def api_delete_book(id):
    book = library.get_book(id)
    if not book:
        abort(404)
    library.delete_book(id)
    return jsonify({'result': book})

@apis.route("/api/v1/books/<int:id>", methods=["PUT"])
def api_update_book(id):
    data = json.loads(request.json)
    book = library.get_book(id)
    if not book:
        abort(404)
    if not data or not utils.valid_post_put(data, post=False):
        abort(400)
    old_book_data = book
    updated_book_data = {
        **dict(
            (k, data.get(k, old_book_data[k])) for k in old_book_data
        )
    }
    book = library.update_book(id, updated_book_data, True)
    return jsonify({'book': book.formatted()})