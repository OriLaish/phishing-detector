from retaraining_component import DB_managment
from datetime import datetime


class URLsDataBase(DB_managment.DataBase):
    def __init__(self, table_name: str):
        super.__init__()
        self._table_name = table_name

    def enter_row(self, url_name: str, submission_date: datetime) -> None:
        self.commit_execute(f'INSERT INTO {self._table_name}(URL, SUBMISSION_DATE,IS_SCRAPED) VALUES({url_name}, {datetime}, N')

    def last_scraped_date(self) -> (bool, datetime):
        ans = self.data_extraction_execute(f"SELECT SUBMISSION_DATE FROM {self._table_name} WHERE IS_SCRAPED = 'Y' OR IS_SCRAPED = 'F'")
