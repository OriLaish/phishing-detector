from django.db import models
from enum import Enum
import asyncio
from .web_scraping import web_scraping
import uuid

SUBMISSION_COUNT_THRESHOLD = 4

class If_Scraped_enum(Enum):
    Yes = "Y"
    No = "N"
    Faild= "F"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class UIDS(models.Model):
    uid = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return f'UID: {self.uid}, id: {self.id}'
    

class URLS(models.Model):
    url = models.URLField(null=False, max_length=500, unique=True)

    def __str__(self):
        return f'URL: {self.url}, id: {self.id}'
    

class UIDS_URLS(models.Model):
    url_id = models.ForeignKey(URLS, null=False, on_delete=models.CASCADE, unique=False) 
    uid_id = models.ForeignKey(UIDS, null=False, on_delete=models.CASCADE, unique=False)

class Phishtank_urls(models.Model):
    url_id = models.ForeignKey(URLS, null=False, on_delete=models.CASCADE, unique=True)
    submission_date = models.DateTimeField(null=False)
    is_scraped = models.CharField( max_length=50 , choices=If_Scraped_enum.choices())

    def __str__(self):
        return f'URL: {self.url_id.url}, submission_date: {self.submission_date}'
    

class Client_urls(models.Model):
    url_id = models.ForeignKey(URLS, null=False, on_delete=models.CASCADE, unique=True)
    is_phishing = models.BooleanField(null=False)
    features = models.CharField( max_length = 100 )
    submission_count = models.IntegerField()
    is_in_web_scraping= models.BooleanField(default=False)
    

class Web_scraping_data(models.Model):
    url_id = models.ForeignKey(URLS, null=False, on_delete=models.CASCADE, unique=True)
    features = models.CharField( max_length= 100 )
    is_phishing = models.BooleanField(null=False)
    is_trained = models.BooleanField(null=False)
    is_from_client = models.BooleanField(null=False)


class Models_Helper:

    @staticmethod
    def get_url_id(url):
        """
        function return the id of the recieved URL
        :param url: the url to find the id of (Str)
        :return: the id of the url or -1 if url not in db (int)
        """
        if URLS.objects.filter(url=url).count() == 0:
            return -1
        return URLS.objects.filter(url=url)[0].id
    
    @staticmethod
    def insert_url(url):
        """
        function enters the url to db and return the id of the recieved URL
        :param url: the urlto insert (Str)
        :return: the id of the url (id)
        """
        if Models_Helper.get_url_id(url) == -1:
            URLS(url=url).save()
        return Models_Helper.get_url_id(url)
    
    @staticmethod
    def create_uid():
        """
        that function creates a new & unique uid saves it in the db and returns it 
        """
        while True:
            new_uid = str(uuid.uuid4())
            if UIDS.objects.filter(uid=new_uid).count() == 0:  # checks if uid is not allready exsiting
                UIDS(uid=new_uid).save()
                return new_uid
    
    @staticmethod
    def insert_uid_url(uid_obj, url_obj):
        """
        that function attempts to enter the uid and url to the uid_url db and returns true if sucsseded and false otherwise
        :params: uid_obj: (UIDS), url_obj: (URLS)
        """
        if UIDS_URLS.objects.filter(uid_id=uid_obj).filter(url_id=url_obj).count() == 0:
            try:
                UIDS_URLS(url_id=url_obj, uid_id=uid_obj).save()
                return True
            except:
                return False
        return False

    @staticmethod
    def insert_phistank_url_line(url, submission_date):
        """
        function enters the phishtank line to db and return True if sucsseded and False otherwise
        :params: url: the url to insert (Str), submission_date: the date of submission to phishtank (datetime)
        :return: bool
        """
        url_id = Models_Helper.insert_url(url)
        try:
            Phishtank_urls(url_id=URLS.objects.filter(id=url_id)[0], submission_date=submission_date, is_scraped=False).save()
            return True
        except:
            return False
    
    @staticmethod
    def insert_client_url_line(uid, url, is_phishing, features):
        """
        that function recieve a url that had been submitted to the server by a client. if the url had allready been submitedit adds to the submission
        count and if not it adds it.
        params: uid: the client uid(Str), url: the url to insert (Str), is_phishing: if the url had been submitted as phishing by the client(bool), features: featrues 
        for model training(Str)
        :return: if insertion secsseded
        """
        
        if Phishtank_urls.objects.filter(url_id=Models_Helper.get_url_id(url)).count() == 1 or type(url) != str or type(is_phishing) != bool or type(features) != str:  # param validation
            return False
        uid_obj = UIDS.objects.get(uid=uid)
        url_obj = URLS.objects.filter(id=Models_Helper.insert_url(url))[0]  # inserts the url to URLS if not exsisting and saving the URL line in var 
        if not Models_Helper.insert_uid_url(uid_obj=uid_obj, url_obj=url_obj):  # inserting uid_url to db if not existing and checking if allready exsisting
            return False
        try:
            url_line = Client_urls.objects.filter(url_id=Models_Helper.get_url_id(url))[0]  # getting url_id if url exsists
            if url_line.is_phishing == is_phishing:  # if the phishing status of the saved and submitted is the same then increase count
                url_line.submission_count = url_line.submission_count + 1
            else:  # else decreas count 
                url_line.submission_count = url_line.submission_count - 1
            url_line.save()
            return True
        except: 
            try:
                Client_urls(url_id=url_obj, features=features, is_phishing=is_phishing, submission_count=1).save()
                return True
            except Exception as e:
                print("## Exception: ", e)
                return False
    
    @staticmethod
    def insert_web_scraping_data_line(url_id, features, is_phishing, is_from_client):
        """
        inserting line to web scraping table (table of featured data for training)
        """
        Web_scraping_data(url_id=url_id, features=features, is_phishing=is_phishing, is_trained= False, is_from_client=is_from_client).save()
        return True
        

    @staticmethod
    def is_url_in_phishtank_urls(url):
        """
        returning if url is in phishtank table
        """
        url_id = Models_Helper.get_url_id(url)
        return url_id == -1 or Phishtank_urls.objects.filter(url_id=url_id).count() != 0
    
    @staticmethod
    def update_client_data_table():
        """
        function updates negetive submission negtive count urls to correct is_phishing type
        """
        for line in Client_urls.objects.filter(submission_count__lt=0):
            line.is_phishing = not line.is_phishing
            line.submission_count = line.submission_count * -1
            line.save()

    @staticmethod
    def add_client_urls_to_scraping_table():
        """
        function adds url that has been submitted by enough users to the list of traineble urls
        """
        for line in Client_urls.objects.filter(submission_count__gte=SUBMISSION_COUNT_THRESHOLD).filter(is_in_web_scraping=False): # lines in correct 
            Models_Helper.insert_web_scraping_data_line(url_id=line.url_id, features=line.features, is_phishing=line.is_phishing, is_from_client=True)
            line.is_in_web_scraping = True
            line.save()
    
    @staticmethod
    def scrape_line(line, event_loop, browser=False):
        """
        scrape line and adds it to web scrapind data table
        """
        try:
            featuresOfURL = event_loop.run_until_complete(web_scraping(line.url_id.url, browser))
        except Exception as e:
            print("## Exception in web scraping:", e)
            return True
        if( Models_Helper.insert_web_scraping_data_line(url_id=line.url_id, features=",".join(str(f) for f in featuresOfURL), is_phishing=True, is_from_client=False)):
            return True
        else:
            return False
        
    

    


        

    






        








