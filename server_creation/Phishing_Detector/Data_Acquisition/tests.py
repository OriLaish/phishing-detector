from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# Using the standard RequestFactory API to create a form POST request


class WidgetTestCase(APITestCase):
    
    def testThis(self):
        self.client = APIClient()
        data = {'url': 'https://www.django-rest-framework.org/api-guide/testing/' , 'is_phishing' : True , 'features' : "1,1,1,0,1,1,1,1,1,0,0,0,-1,-1,1"}
        response = self.client.post("/submit_url" , data)
        self.assertEqual(response.status_code , status.HTTP_201_CREATED)






    


