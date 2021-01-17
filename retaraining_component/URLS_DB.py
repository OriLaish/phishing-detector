from retaraining_component import DB_managment
from datetime import datetime


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


class URLsDataBase(DB_managment.DataBase):

    def __init__(self, table_name: str):
        DB_managment.DataBase.__init__(self)
        self._table_name = table_name

    def enter_row(self, url_name: str, submission_date: datetime) -> None:
        """
        enters a URL row to the DB
        :param url_name: the URL path
        :param submission_date: the URL submission date
        :return: None
        """
        self.commit_execute(
            query=f"INSERT INTO {self._table_name}(URL, SUBMISSION_DATE, IS_SCRAPED) "
                  f"VALUES('{url_name}', '{submission_date}', 'N')")

    def last_scraped_date(self) -> (bool, datetime):
        """
        :return: returns the datetime of the last item in the DB that haven't been scraped
        """
        ans = self.data_extraction_execute(
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
        ans = self.data_extraction_execute(
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
        ans = self.data_extraction_execute(
            f"SELECT SUBMISSION_DATE FROM {self._table_name} WHERE IS_SCRAPED = 'N'")
        if ans[0]:
            return len(ans[1])
        return -1


# db_conn = URLsDataBase("PHISHING_URLS")
# db_conn.enter_row("test_3", datetime.now())
# print(db_conn.last_scraped_date()[1])
