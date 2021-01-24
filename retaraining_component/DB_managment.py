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


class URLInfo:
    def __init__(self, url_name: str, date: datetime, is_scraped: str):
        self._url_name = url_name
        self._submission_date = date
        self._is_scraped = is_scraped

    def __init__(self, values: list):
        self._url_name = values[0]
        self._submission_date = values[1]
        self._is_scraped = values[2]

    def get_submission_date(self) -> datetime:
        """
        :return: submission date column if it is d datetime and None otherwise
        """
        if type(self._submission_date) is datetime:
            return self._submission_date
        return None


class UrlsDataBase:

    def __init__(self, table_name: str = "URLS"):
        """
        :param table_name: the name of the table
        """
        self._db = DataBase()
        self._table_name = table_name

    def enter_row(self, url_name: str, submission_date: datetime) -> None:
        """
        enters a URL row to the DB
        :param url_name: the URL path
        :param submission_date: the URL submission date
        :return: None
        """
        self._db.commit_execute(
            query=f"INSERT INTO {self._table_name}(URL, SUBMISSION_DATE, IS_SCRAPED) "
                  f"VALUES('{url_name}', '{submission_date}', 'N')")

    def last_scraped_date(self) -> (bool, datetime):
        """
        :return: returns the datetime of the last item in the DB that haven't been scraped
        """
        ans = self._db.data_extraction_execute(
            f"SELECT * FROM {self._table_name} WHERE IS_SCRAPED = 'Y' OR IS_SCRAPED = 'F'"
            f" ORDER BY SUBMISSION_DATE DESC LIMIT 1")
        if ans[0] and len(ans[1]) > 0:
            last_line = URLInfo(ans[1][-1])  # gets last inserted & scraped line
            if last_line.get_submission_date() is not None:
                return True, last_line.get_submission_date()
        return False, None

    def last_entered_date(self) -> (bool, datetime):
        """
        :return: returns the date of the last entered url to the DB as datetime
        """
        ans = self._db.data_extraction_execute(
            f"SELECT * FROM {self._table_name} ORDER BY SUBMISSION_DATE DESC LIMIT 1")
        if ans[0] and len(ans[1]) > 0:
            last_line = URLInfo(ans[1][0])  # gets last inserted & scraped line
            if last_line.get_submission_date() is not None:
                return True, last_line.get_submission_date()
        return False, None

    def unscraped_len(self) -> int:
        """
        :return: returns the amount of unscraped URLS in the DB
        """
        ans = self._db.data_extraction_execute(
            f"SELECT SUBMISSION_DATE FROM {self._table_name} WHERE IS_SCRAPED = 'N'")
        if ans[0]:
            return len(ans[1])
        return -1

    def update_scraping_status(self, url: str, new_status: str) -> bool:
        """
        updating the url is_scraped column
        :param url: the url to update
        :param new_status: the new status
        :return: were the updating successful
        """
        if new_status not in ['Y', 'N', 'F']:  # checks if the new status is a possible option
            return False
        return self._db.commit_execute(
            f"UPDATE {self._table_name} SET IS_SCRAPED = '{new_status}' WHERE URL = '{url}';")


class ScrapedDataInfo:

    def __init__(self, primary_id: int, url_id: int, url_type: str, features: str, is_scraped: str):
        self._primary_id = primary_id
        self._url_id = url_id
        self._url_type = url_type
        self._is_scraped = is_scraped
        try:
            self._features = [int(x) for x in features.split('#')]
        except:
            self._features = None
        finally:
            if len(self._features) != 15:  # amount of features
                self._features = None

    def __str__(self):
        return f"id: {self._primary_id}, url_id:{self._url_id}, type: {self._url_type}, is scraped: " \
               f"{self._is_scraped}  features: {self._features}"

    def __repr__(self):
        return self.__str__()


class ScrapedDataDataBase:

    def __init__(self):
        self._db = DataBase()

    def enter_row(self, url_id: int, url_type: str, features: list) -> bool:
        """
        enter new row to the data base
        :param url_id: the id of the url in the phishing or legit DBs
        :param url_type: either phisihing (P) or legit (L)
        :param features: the scraped features
        :return: bool of whether the insertion was successful
        """
        if url_type not in ['P', 'L'] or len(features) != 15 or type(url_id) == int:  # checks if data to enter is ok
            return False
        print(f"INSERT INTO SCRAPED_DATA (URL_ID, TYPE , FEATURES, IS_TRAINED) VALUES ("
              f"{url_id}, '{url_type}', '{'#'.join([str(x) for x in features])}', 'N')")
        return self._db.commit_execute(f"INSERT INTO SCRAPED_DATA (URL_ID, TYPE , FEATURES, IS_TRAINED) VALUES ("
                                       f"{url_id}, '{url_type}', '{'#'.join([str(x) for x in features])}', 'N')")

    def update_training_status(self, primary_id: int) -> bool:
        """
        updating the row with the given id to scraped
        :param primary_id: the id
        :return: whether the change was successful
        """
        if type(id) != int:
            return False
        return self._db.commit_execute(
            f"UPDATE SCRAPED_DATA SET IS_TRAINED = 'Y' WHERE ID = {primary_id};")

    def get_traineble_data(self) -> (bool, list):
        """
        receiving all data that model hasn't been trained on yet
        :return: the data as list of ScrapedDataaBaseInfo
        """
        data = self._db.data_extraction_execute("SELECT * FROM SCRAPED_DATA WHERE IS_TRAINED = 'N'")
        if not data[0]:
            return False, None
        return True, [ScrapedDataInfo(url_id=line[0], url_type=line[1], features=line[2], is_scraped=line[3], primary_id=line[4]) for line
                      in data[1]]


def create_tables(db: DataBase):
    db.reg_execute("DROP TABLE PHISHING_URLS")
    db.reg_execute("DROP TABLE LEGIT_URLS")
    db.reg_execute("CREATE TABLE PHISHING_URLS(URL varchar(500), SUBMISSION_DATE datetime, IS_SCRAPED ENUM('Y', 'N',"
                   " 'F'), URL_ID int PRIMARY KEY AUTO_INCREMENT)")
    db.reg_execute("CREATE TABLE LEGIT_URLS(URL varchar(500), SUBMISSION_DATE datetime, IS_SCRAPED ENUM('Y', 'N', 'F')"
                   ", URL_ID int PRIMARY KEY AUTO_INCREMENT)")
    db.reg_execute("CREATE TABLE SCRAPED_DATA(URL_ID int, TYPE ENUM('P', 'L'), FEATURES VARCHAR(46), IS_TRAINED ENUM"
                   "('Y', 'N'), ID int PRIMARY KEY AUTO_INCREMENT)")

