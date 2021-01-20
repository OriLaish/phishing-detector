import requests
import pandas as pd
import csv

URL_DB = "http://data.phishtank.com/data/online-valid.csv"


def get_updated_db():
    df = pd.read_csv(URL_DB)
    df.to_csv('db.csv')


get_updated_db()
