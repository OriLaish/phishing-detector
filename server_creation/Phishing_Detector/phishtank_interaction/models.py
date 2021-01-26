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

