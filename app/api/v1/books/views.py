from flask import jsonify, request
from . import books as books_bp

from app.domain.books.utils import build_book, get, get_all, add, delete, update
from utils import to_dict


@books_bp.route("/<isbn>", methods=["GET"])
def get_book(isbn: str):
    book = get(isbn)

    if book:
        return jsonify(to_dict(book))
    else:
        return jsonify({"message": f"Book with isbn {isbn} not found."}), 404


@books_bp.route("/", methods=["GET"])
def get_all_books():
    books = get_all()
    result = list()
    for book in books:
        result.append(to_dict(book))
    return jsonify({
        "number_results": len(books),
        "books": result
    }), 200


@books_bp.route("/", methods=["POST"])
def create_book():
    data = request.get_json()
    book = get(isbn=data.get('isbn'))
    if book is None:
        book = build_book(data)
        add(book)
        return jsonify({"message": f"Book with isbn {data.get('isbn')} created successfully."}), 201
    else:
        return jsonify({"message": f"Book with isbn {data.get('isbn')} already exists."}), 409


@books_bp.route("/<isbn>", methods=["DELETE"])
def delete_book(isbn: str):
    status = delete(isbn)
    print(status)
    if status == 1:
        return jsonify({"message": f"Book with isbn {isbn} deleted."}), 204
    else:
        return jsonify({"message": f"Book with isbn {isbn} not found."}), 404


@books_bp.route("/<isbn>", methods=["PUT"])
def update_book(isbn: str):
    book = get(isbn)
    if book:
        data = request.get_json()
        status = update(book, data)
        if status == 1:
            return jsonify({"message": f"Book {isbn} updated successfully."}), 200
        else:
            return jsonify({"message": f"Something went wrong while updating book {isbn}."}), 500
    else:
        return jsonify({"message": f"Book {isbn} not found."}), 404
