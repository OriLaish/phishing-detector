from django.urls import path
from .views import main
from . import views

urlpatterns = [
    path('', main),
    path('submit_url', views.client_url_submission_api.as_view())
]