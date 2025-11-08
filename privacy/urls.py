from django.urls import path
from privacy.views import privacy_notice_view

app_name = "privacy"

urlpatterns = [
    path("", privacy_notice_view, name="notice"),
]
