from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('submit_url', views.client_url_submission_api.as_view()),
    path('update_phishtank_db', views.phishtank_url_db_update),
    path('scrape_new_urls', views.scrape_new_urls),
    path('get_model', views.serve_model)
]