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
from .serializers import client_submission_data, client_submission_data_serializer
from rest_framework.parsers import JSONParser
from io import StringIO
import asyncio
from .web_scraping import web_scraping
import pyppeteer


PHISHTANK_URL = "http://data.phishtank.com/data/online-valid.csv"
TEMP_LOC = "tempTank.csv"

def main(request):
    
    return HttpResponse('hello')


def phishtank_url_db_update(request):
    """
    interacts with phishtank API and inserts new phishing urls to local DB
    """
    startTime = datetime.datetime.now()
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
    endTime = datetime.datetime.now()
    TotalTime = endTime - startTime
    return HttpResponse(f"It took (in seconds): {TotalTime.seconds}")


def scrape_new_urls(request):
    """
    scrape all unscraped urls in server
    """
    startTime = datetime.datetime.now()
    unscraped_urls = Phishtank_urls.objects.filter(is_scraped=False)
    browser = asyncio.new_event_loop().run_until_complete(pyppeteer.launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False))
    for line in unscraped_urls:
        if Models_Helper.scrape_line(line):
            line.is_scraped = True
            line.save()
    asyncio.new_event_loop().run_until_complete(browser.close())
    endTime = datetime.datetime.now()
    TotalTime = endTime - startTime
    return HttpResponse(f"It took (in seconds): {TotalTime.seconds}")
    




class client_url_submission_api(APIView):

    serializer_class = client_submission_data_serializer

    def post(self, request, format=None):
        """
        handeling url submission from clients
        """
        request_info_serialzer = client_submission_data_serializer(data=request.data)
        print(request.data)
        if not request_info_serialzer.is_valid():
            print(request_info_serialzer.errors)
            return Response({'Bad Request': f'failed to process requrst - {request_info_serialzer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
        request_info_serialzer.save()
        print(f"url={request_info_serialzer.data.get('url')}, is_phishing={request_info_serialzer.data.get('is_phishing')}, features={request_info_serialzer.data.get('features')}")  
        if Models_Helper.insert_client_url_line(url=request_info_serialzer.data.get('url'), is_phishing=request_info_serialzer.data.get('is_phishing'), features=request_info_serialzer.data.get('features')):
            return Response({'message': 'url submitted sucssefully'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'Bad Request': 'failed to submit url'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request, format=None):
        return Response({'Bad Request': 'Only available as post requests'}, status=status.HTTP_400_BAD_REQUEST)
    




    