import mysql.connector
from databases.model import Topics, Books, Description
import os


class DB:
    def __init__(self) -> None:
        self.img_default = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRheXK2LAz36tgp5K8LuaSaab_vj_tQmi1J8zv6qe4IhFykh_Sz"
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
        if cover is None or cover == "":
            return self.img_default

        base = "https://library.lol/covers/"

        return base + cover

    def _update_md5(self, md5: str):
        if md5 is None or md5 == "":
            return self.img_default

        base = "https://library.lol/main/"

        return base + md5

    def _update_topic(self, topic_id) -> dict | str:
        if topic_id == 0 or topic_id == "":
            return "Tópico Não Encontrado"

        self.cursor.execute(
            f"SELECT topic_descr from topics where lang = 'en' and topic_id = {topic_id};"
        )
        resp: dict | None = self.cursor.fetchone()
        topic: str = ""
        if resp:
            topic = resp.get("topic_descr", "Tópico Não Encontrado")
            topic = topic.replace("\\\\", " -> ")
        return topic

    def _formatter_subtopics(self, string: str):
        lista_string = string.split("\\\\")
        try:
            return lista_string[1]
        except Exception:
            return lista_string[0]

    def select_by_id_list(self, id_list) -> list[dict]:
        list_resp = []
        for id_ in id_list:
            self.cursor.execute(
                f"""SELECT ID, Title,Series,Author, 
                    Year,Edition,Publisher,Pages,Language,Identifier,
                    Filesize,MD5,Coverurl,Topic
                    FROM books WHERE ID = {id_};"""
            )

            resp: dict[Books, str | int] | None = self.cursor.fetchone()
            if resp:
                resp["Topic"] = self._update_topic(resp.get("Topic", 0))
                resp["MD5"] = self._update_md5(resp.get("MD5", ""))
                resp["Coverurl"] = self._update_coverurl(resp.get("Coverurl", ""))

            list_resp.append(resp)

        return list_resp

    def _select_description(self, md5) -> str:
        self.cursor.execute(f"SELECT descr FROM description WHERE md5 = '{md5}';")
        response: dict[Description, str | int] | None = self.cursor.fetchone()
        if response is None:
            return ""
        return bytes.decode(response.get("descr", ""), encoding="UTF-8")

    def select_by_id(self, id_):
        self.cursor.execute(
            f"""SELECT ID, Title,Series,Author, 
                Year,Edition,Publisher,Pages,Language,Identifier,
                Filesize,MD5,Coverurl,Topic
                FROM books WHERE ID = {id_};"""
        )

        resp: dict[Books, str | int] | None = self.cursor.fetchone()
        if resp:
            resp["Topic"] = self._update_topic(resp.get("Topic", 0))
            resp["descr"] = self._select_description(resp.get("MD5"))
            resp["MD5"] = self._update_md5(resp.get("MD5", ""))
            resp["Coverurl"] = self._update_coverurl(resp.get("Coverurl", ""))

        return resp

    def select_topics(self):
        self.cursor.execute(
            """select topic_id_hl, topic_descr 
                from topics 
                where lang = 'en' and topic_id 
                    in (SELECT topic_id_hl FROM topics group by topic_id_hl);"""
        )

        resp: dict[Topics, str | int] | None = self.cursor.fetchall()
        return resp

    def select_subtopics(self, id_: int):
        self.cursor.execute(
            f"""select topic_descr 
                from topics 
                where topic_id_hl = {id_} 
                    and lang = 'en' and topic_id_hl != topic_id;"""
        )
        resp: list[Topics] | None = self.cursor.fetchall()
        if resp:
            for item in resp:
                item["topic_descr"] = self._formatter_subtopics(item.get("topic_descr"))

        return resp
