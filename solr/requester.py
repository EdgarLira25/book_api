import requests
from typing import Literal
import json


class SolrRequester:

    base_url = "http://127.0.0.1:8983/solr/"
    endpoint = "query"
    page_size = 12

    def __init__(
        self,
        core: Literal[
            "books_title",
            "books_author",
            "books_filters",
            "books_isbn",
        ],
    ) -> None:
        self.core = core

    def request_query(
        self,
        text: str,
        page: int,
    ) -> list[dict]:
        params = {
            "q": text,
            "q.op": "OR",
            "indent": "true",
            "rows": self.page_size,
            "start": page * self.page_size,
        }

        url = f"{self.base_url}{self.core}/{self.endpoint}"

        response = requests.get(url, params=params).json()

        solr_list = []
        pages = response.get("response").get("numFound", 0) // self.page_size
        for dicionary in response.get("response")["docs"]:
            solr_list.append(json.loads(dicionary.get("_src_")).get("ID"))

        return solr_list, pages
