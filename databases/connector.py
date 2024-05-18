import mysql.connector
from databases.model import Topics, Books, Description
import os


class DB:

    def __init__(self) -> None:
        self.con = mysql.connector.connect(
            host="localhost",
            database="lib",
            user="edgarlira",
            password=os.environ.get("PASSWORD"),
            port=3306,
            auth_plugin="mysql_native_password",
        )
        self.cursor = self.con.cursor(dictionary=True)

    def _update_coverurl(self, cover: str):
        base = "https://library.lol/covers/"

        return base + cover

    def _update_md5(self, md5: str):
        base = "https://library.lol/main/"

        return base + md5

    def _formatter_subtopics(self, string: str):
        lista_string = string.split("\\\\")
        try:
            return lista_string[1]
        except:
            return lista_string[0]

    def select_by_id_list(self, id_list) -> list[dict]:

        list_resp = []
        for id_ in id_list:
            self.cursor.execute(
                f"""SELECT ID, Title,Series,Author, 
                    Year,Edition,Publisher,Pages,Language,Identifier,
                    Filesize,MD5,Coverurl
                    FROM books WHERE ID = {id_};"""
            )

            resp: dict[Books] = self.cursor.fetchone()
            resp["MD5"] = self._update_md5(resp.get("MD5", ""))
            resp["Coverurl"] = self._update_coverurl(resp.get("Coverurl", ""))

            list_resp.append(resp)

        return list_resp

    def _select_description(self, md5) -> str:

        self.cursor.execute(f"SELECT descr FROM description WHERE md5 = '{md5}';")
        response: dict[Description] = self.cursor.fetchone()
        return bytes.decode(response.get("descr", ""), encoding="UTF-8")

    def select_by_id(self, id_):

        self.cursor.execute(
            f"""SELECT ID, Title,Series,Author, 
                Year,Edition,Publisher,Pages,Language,Identifier,
                Filesize,MD5,Coverurl 
                FROM books WHERE ID = {id_};"""
        )

        resp: dict[Books] = self.cursor.fetchone()

        resp["descr"] = self._select_description(resp.get("MD5"))
        resp["MD5"] = self._update_md5(resp.get("MD5", ""))
        resp["Coverurl"] = self._update_coverurl(resp.get("Coverurl", ""))

        return resp

    def select_topics(self):

        self.cursor.execute(
            f"""select topic_id_hl, topic_descr 
                from topics 
                where lang = 'en' and topic_id 
                    in (SELECT topic_id_hl FROM topics group by topic_id_hl);"""
        )

        resp: dict[Topics] = self.cursor.fetchall()
        return resp

    def select_subtopics(self, id_: int):

        self.cursor.execute(
            f"""select topic_descr 
                from topics 
                where topic_id_hl = {id_} 
                    and lang = 'en' and topic_id_hl != topic_id;"""
        )
        resp: list[Topics] = self.cursor.fetchall()

        for item in resp:
            item["topic_descr"] = self._formatter_subtopics(item.get("topic_descr"))

        return resp
