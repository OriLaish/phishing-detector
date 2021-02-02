from django.shortcuts import render
import pandas as pd
import csv
import datetime
from Data_Acquisition.models import urlDB
from Data_Acquisition.models import If_Scraped_enum
from rest_framework import generics
from django.http import HttpResponse


PHISHTANK_URL = "http://data.phishtank.com/data/online-valid.csv"
TEMP_LOC = "tempTank.csv"

# Create your views here.
def main(requset):
    

    phishtank_df = pd.read_csv(PHISHTANK_URL)
    try:
        last_entered_date = urlDB.objects.latest('Submission_Date')

    except:
        last_entered_date = False
        
    for line in phishtank_df.values:
        date = datetime.datetime.strptime(line[3].split("+")[0], '%Y-%m-%dT%H:%M:%S')
        if ( not last_entered_date or date > last_entered_date.Submission_Date )  and ( urlDB.objects.filter(URL = line[1]).count() == 0 ) :
            url = line[1]
            added_line = urlDB(URL=url, Submission_Date=date ,Is_scraped = 'N', Is_Phishing=True )
            added_line.save()
        else:
           break
    
    return HttpResponse("Hello")



    