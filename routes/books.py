from flask import Response, jsonify, Blueprint
from controllers.books import BooksController
from typing import Literal
books_blueprint = Blueprint("books", __name__)


@books_blueprint.route(
    "/book/<string:core_type>/<string:query>/<int:page>", methods=["GET"]
)
def query_books(core_type: Literal["title", "author", "filters", "isbn"], query: str, page: int) -> tuple[Response, int]:
    controller = BooksController(core="books_" + core_type)
    response, pages = controller.books_query(query, page)

    return jsonify(book=response, pages=pages), 200


@books_blueprint.route("/book/<int:id>", methods=["GET"])
def query_book_by_id(id: int) -> tuple[Response, int]:
    controller = BooksController()
    response = controller.book_by_id(id)

    return jsonify(book=response), 200


@books_blueprint.route("/topics", methods=["GET"])
def get_topics():

    controller = BooksController()
    response = controller.topics()

    return jsonify(topics=response)


@books_blueprint.route("/topics/<int:id>", methods=["GET"])
def get_sub_topics(id: int):

    controller = BooksController()
    response = controller.sub_topics(id)

    return jsonify(topics=response)


@books_blueprint.route("/", methods=["GET"])
def root():
    return "<h1> He is alive </h1>"
