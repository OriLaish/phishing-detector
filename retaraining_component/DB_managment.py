import asyncio
import pymysql
from datetime import datetime


class DataBase:

    def __init__(self):

        self._conn = pymysql.connect(host="localhost", user="root", password="root", db="test")
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
    db.reg_execute("DROP TABLE PHISHING_URLS")
    db.reg_execute("DROP TABLE LEGIT_URLS")
    db.reg_execute("CREATE TABLE PHISHING_URLS(URL varchar(500), SUBMISSION_DATE datetime, IS_SCRAPED ENUM('Y', 'N', 'F'), URL_ID int PRIMARY KEY AUTO_INCREMENT)")
    db.reg_execute("CREATE TABLE LEGIT_URLS(URL varchar(500), SUBMISSION_DATE datetime, IS_SCRAPED ENUM('Y', 'N', 'F'), URL_ID int PRIMARY KEY AUTO_INCREMENT)")


db1 = DataBase()
create_tables(db1)
