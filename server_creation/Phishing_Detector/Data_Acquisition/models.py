from django.db import models
from enum import Enum

class If_Scraped_enum(Enum):
    Yes = "Y"
    No = "N"
    Faild= "F"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class URLS(models.Model):
    URL = models.CharField(null=False, max_length=500, unique=True)

    def __str__(self):
        return f'URL: {self.URL}, id: {self.id}'
    



class Phishtank_urls(models.Model):
    URL_ID = models.ForeignKey(URLS, null=False, on_delete=models.CASCADE, unique=True)
    Submission_Date = models.DateTimeField(null=False)
    Is_scraped = models.CharField( max_length=50 , choices=If_Scraped_enum.choices())

    def __str__(self):
        return f'URL: {self.URL_ID.URL}, submission_date: {self.Submission_Date}'
    

class Client_urls(models.Model):
    URL_ID = models.ForeignKey(URLS, null=False, on_delete=models.CASCADE, unique=True)
    Is_Phishing = models.BooleanField(null=False)
    Features = models.CharField( max_length = 100 )
    Submission_Count = models.IntegerField()
    

class Web_scraping_data(models.Model):
    urlId = models.ForeignKey(URLS, null=False, on_delete=models.CASCADE, unique=True)
    Features = models.CharField( max_length= 100 )
    Is_Phishing = models.BooleanField(null=False)
    Is_Trained = models.BooleanField(null=False)
    Is_From_Client = models.BooleanField(null=False)


class Models_Helper:

    @staticmethod
    def get_url_id(url):
        """
        function return the id of the recieved URL
        :param url: the url to find the id of (Str)
        :return: the id of the url or -1 if url not in db (int)
        """
        if URLS.objects.filter(URL=url).count() == 0:
            return -1
        return URLS.objects.filter(URL=url)[0].id
    
    @staticmethod
    def insert_url(url):
        """
        function enters the url to db and return the id of the recieved URL
        :param url: the urlto insert (Str)
        :return: the id of the url or -1 if url not in db (int)
        """
        if Models_Helper.get_url_id(url) == -1:
            URLS(URL=url).save()
        return Models_Helper.get_url_id(url)

    @staticmethod
    def insert_phistank_url_line(url, submission_date):
        """
        function enters the phishtank line to db and return True if sucsseded and False otherwise
        :params: url: the url to insert (Str), submission_date: the date of submission to phishtank (datetime)
        :return: bool
        """
        url_id = Models_Helper.insert_url(url)
        try:
            Phishtank_urls(URL_ID=URLS.objects.filter(id=url_id)[0], Submission_Date=submission_date, Is_scraped=False).save()
            return True
        except:
            return False
    
    @staticmethod
    def insert_client_url_line(url, is_phishing, features):
        """
        that function recieve a url that had been submitted to the server by a client. if the url had allready been submitedit adds to the submission
        count and if not it adds it.
        params: url: the url to insert (Str), is_phishing: if the url had been submitted as phishing by the client(bool), features: featrues for model 
        training(Str)
        :return: if insertion secsseded
        """
        if Phishtank_urls.objects.filter(URL_ID=Models_Helper.get_url_id(url)).count() == 1:
            return False
        try:
            url_line = Client_urls.objects.filter(URL_ID=Models_Helper.get_url_id(url))[0]
            if url_line.Is_Phishing == is_phishing:  # if the phishing status of the saved and submitted is the same then increase count
                url_line.Submission_Count += 1
            else:  # else decreas count 
                url_line.Submission_Count -= 1
            url_line.save()
            return True
        except:
            url_id = Models_Helper.insert_url(url)
            try:
                Client_urls(URL_ID=URLS.objects.filter(id=url_id)[0], Features=features, Is_Phishing=is_phishing, Submission_Count=1).save()
                return True
            except:
                return False
        

    






        








