import asyncio
import pymysql
from datetime import datetime


class DataBase:

    def __init__(self):
        self._conn = pymysql.connect(host="localhost", user="root", passwd="root", database="test")
        self._cursor = self._conn.cursor()

    def reg_execute(self, query: str = "") -> bool:
        """
        executing a regular query that don't require committing or returning data
        :param query: the query to execute
        :return: whether the the query execution succeeded
        """
        if query == "":
            print("Error: empty query")
            return False
        else:
            try:
                self._cursor.execute(query)
            except:
                print("ERROR: query failed")
                return False
            return True

    def commit_execute(self, query: str = "") -> bool:
        """
        executing a query that requires committing and commiting to db if query succeeded
        :param query: the query to execute
        :return: whether the the query execution succeeded
        """
        if self.reg_execute(query):
            self._conn.commit()
            return True
        return False

    def data_extraction_execute(self, query: str = "") -> (bool, list):
        """
        executing a query that requires returning data and  returning data as list[str] if query succeeded
        :param query: the query to execute
        :return: whether the the query execution succeeded and the extracted data
        """
        if self.reg_execute(query):
            return True, [x for x in self._cursor]
        return False, []


def create_tables(db: DataBase):
    db.execute("CREATE TABLE PHISHING_URLS(URL varchar(50), DATE_OF_SUB datetime, IS_SCRAPED tinyint, URL_ID int PRIMARY KEY AUTO_INCREMENT)")
    db.execute("CREATE TABLE LEGIT_URLS(URL varchar(50), DATE_OF_SUB datetime, IS_SCRAPED tinyint, URL_ID int PRIMARY KEY AUTO_INCREMENT)")


# db1: DataBase = DataBase()
# ans = db1.data_extraction_execute("DESCRIBE PHISHING_URLS")
# for x in ans[1]:
#    print(x)
