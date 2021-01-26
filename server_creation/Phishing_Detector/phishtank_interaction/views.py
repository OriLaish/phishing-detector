from django.shortcuts import render
import pandas as pd
import csv
import datetime
from phishtank_interaction.models import urlDB
from phishtank_interaction.models import If_Scraped_enum
from rest_framework import generics
from django.http import HttpResponse


PHISHTANK_URL = "http://data.phishtank.com/data/online-valid.csv"
TEMP_LOC = "tempTank.csv"

# Create your views here.
def main(requset):
    

    phishtank_df = pd.read_csv(PHISHTANK_URL)
    last_entered_date = urlDB.objects.latest('Submission_Date')
    for line in phishtank_df.values:
        date = datetime.datetime.strptime(line[3].split("+")[0], '%Y-%m-%dT%H:%M:%S')
        if date > last_entered_date.Submission_Date:
            url = line[2]
            added_line = urlDB(URL=url, Submission_Date=date ,Is_scraped = 'N', Is_Phishing=True )
            added_line.save()
        else:
            break
    return HttpResponse("Hello")



    