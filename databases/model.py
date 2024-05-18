from typing import NamedTuple
from datetime import datetime
			

class Updated(NamedTuple):
    ID: int
    Author: str
    Coverurl: str
    Title: str
    Edition: str
    Filesize: int
    Language: str
    MD5: str
    Pages: str
    Publisher: str
    Series: str
    Topic: str
    VolumeInfo: str
    Year: str
    # Colunas Não Usadas
    Periodical: str
    City: str
    PagesInFile: int
    Library: str
    Issue: str
    Identifier: str
    ISSN: str
    ASIN: str
    UDC: str
    LBC: str
    DDC: str
    LCC: str
    Doi: str
    Googlebookid: str
    OpenLibraryID: str
    Commentary: str
    DPI: int
    Color: str
    Cleaned: str
    Orientation: str
    Paginated: str
    Scanned: str
    Bookmarked: str
    Searchable: str
    Extension: str
    Visible: str
    Locator: str
    Local: int
    TimeAdded: datetime
    TimeLastModified: datetime
    Tags: str
    IdentifierWODash: str


class Topics(NamedTuple):
    id: int
    topic_descr: str
    lang: str
    kolxoz_code: str
    topic_id: int
    topic_id_hl: int


class Description(NamedTuple):
    id: int
    md5: str
    descr: str
    toc: str
    TimeLastModified: datetime
