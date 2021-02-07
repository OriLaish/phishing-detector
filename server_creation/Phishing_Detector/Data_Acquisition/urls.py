from django.urls import path
from .views import main
from .views import client_submission_data

urlpatterns = [
    path('', main),
    path('submit_url', client_submission_data)
]