from django.shortcuts import render
import pandas as pd
import csv
import datetime
from .models import URLS
from .models import If_Scraped_enum
from .models import Phishtank_urls
from .models import Client_urls
from .models import Web_scraping_data
from .models import Models_Helper
from .web_scraping import web_scraping
from rest_framework import generics
from django.http import HttpResponse


PHISHTANK_URL = "http://data.phishtank.com/data/online-valid.csv"
TEMP_LOC = "tempTank.csv"

# Create your views here.
def main(requset):
    
    """
    phishtank_df = pd.read_csv(PHISHTANK_URL)
    try:
        last_entered_date = urlDbb.objects.latest('Submission_Date')

    except:
        last_entered_date = False
        
    for line in phishtank_df.values:
        date = datetime.datetime.strptime(line[3].split("+")[0], '%Y-%m-%dT%H:%M:%S')
        if ( not last_entered_date or date > last_entered_date.Submission_Date )  and ( urlDbb.objects.filter(URL = line[1]).count() == 0 ) :
            url = line[1]
            added_line = urlDbb(URL=url, Submission_Date=date ,Is_scraped = 'N', Is_Phishing=True )
            added_line.save()
        else:
           break
    """
    # Models_Helper.insert_url("test2")
    return HttpResponse(Phishtank_urls.objects.filter(URL_ID=3))



    