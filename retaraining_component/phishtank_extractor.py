import pandas as pd
import csv
import datetime
import retaraining_component.URLS_DB

PHISHTANK_URL= "http://data.phishtank.com/data/online-valid.csv"
TEMP_LOC = "tempTank.csv"




def main():
    db_conn = retaraining_component.URLS_DB.URLsDataBase("PHISHING_URLS")
    last_entered_date = db_conn.last_entered_date(PHISHTANK_URL)
    phishtank_df = pd.read_csv()
    for line in phishtank_df.values:
        date = datetime.datetime.strptime(line[4].split("+")[0], '%Y-%m-%dT%H:%M:%S')
        if date > last_entered_date:
            url = line[2]
            db_conn.enter_row(url_name=url, submission_date=date)
        else:
            break


if  __name__ == '__main__':
    main()



