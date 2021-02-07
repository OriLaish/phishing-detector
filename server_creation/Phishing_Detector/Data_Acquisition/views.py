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
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .data_classes import client_submission_data



PHISHTANK_URL = "http://data.phishtank.com/data/online-valid.csv"
TEMP_LOC = "tempTank.csv"

def main(request):
    return HttpResponse('hello')


# Create your views here.
def phishtank_url_db_update():
    
    phishtank_df = pd.read_csv(PHISHTANK_URL)
    try:
        last_entered_date = Phishtank_urls.objects.latest('submission_date').submission_date

    except:
        last_entered_date = False
        
    for line in phishtank_df.values:
        url = line[1]
        date = datetime.datetime.strptime(line[3].split("+")[0], '%Y-%m-%dT%H:%M:%S')
        if ( not last_entered_date or date > last_entered_date )  and Models_Helper.is_url_in_phishtank_urls(url) :
            Models_Helper.insert_phistank_url_line(url=url, submission_date=date)
        else:
           break
    #Models_Helper.insert_client_url_line("test3", True, "3dd")
    return HttpResponse(Models_Helper.insert_client_url_line("test4", False, "3dd"))

def client_url_submission(request):
    request_info = client_submission_data(request)
    if not request_info.is_secceded:
        return Response({'Bad Request': 'failed to process requrst'}, status=status.HTTP_400_BAD_REQUEST)
    check = Models_Helper.insert_client_url_line(url=request_info.url, is_phishing=request_info.is_phishing, features=request_info.features)
    if check:
        return Response({'message': 'url submitted sucssefully'}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'Bad Request': 'failed to submit url'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    




    