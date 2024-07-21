from solr.requester import SolrRequester
from databases.connector import DB
from typing import Literal


class BooksController:
    def __init__(
        self,
        core: Literal[
            "books_title", "books_author", "books_filters", "books_isbn", ""
        ] = "",
    ) -> None:
        self.core = core

    def books_query(self, query: str, page: int) -> tuple[list[dict], int]:
        solr = SolrRequester(core=self.core)
        list_solr, pages = solr.request_query(text=query, page=page)
        return DB().select_by_id_list(list_solr), pages

    def book_by_id(self, id_: int):
        return DB().select_by_id(id_=id_)

    def topics(self):
        return DB().select_topics()

    def sub_topics(self, id_: int):
        return DB().select_subtopics(id_=id_)
