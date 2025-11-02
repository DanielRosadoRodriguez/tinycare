from django.urls import path
from pages.views.home import home

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
]
