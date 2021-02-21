from django.urls import path
from .views import main
from . import views

urlpatterns = [
    path('', main),
    path('submit_url', views.client_url_submission_api.as_view()),
    path('update_phishtank_db', views.phishtank_url_db_update),
    path('scrape_new_urls', views.scrape_new_urls),
    path('get_model', views.serve_model)
]