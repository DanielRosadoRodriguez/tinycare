# accounts/urls.py
from django.urls import path
from accounts.views.register import register_view

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
]
