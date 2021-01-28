from django.db import models
from enum import Enum

class If_Scraped_enum(Enum):
    Yes = "Y"
    No = "N"
    Faild= "F"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

# Create your models here.
class urlDB(models.Model):
    

    URL = models.CharField(null=False, max_length=500, unique=True)
    Submission_Date = models.DateTimeField(null=False)
    Is_scraped = models.CharField( max_length=50 , choices=If_Scraped_enum.choices())
    Is_Phishing = models.BooleanField(null=False)


class ClientUrlDb(models.Model):
    URL = models.CharField(null=False, max_length=500, unique=True)
    Is_scraped = models.CharField( max_length=50 , choices=If_Scraped_enum.choices())
    Is_Phishing = models.BooleanField(null=False)
    Features = models.CharField( max_length = 100 )
    

    

class webScraingDB(models.Model):
    urlId = models.ForeignKey( urlDB ,  on_delete=models.CASCADE)
    URL = models.CharField(null=False, max_length=500, unique=True)
    Features = models.CharField( max_length= 100 )
    Is_Phishing = models.BooleanField(null=False)
    Is_Trained = models.BooleanField(null=False)
    Is_From_Client = models.BooleanField(null=False)






