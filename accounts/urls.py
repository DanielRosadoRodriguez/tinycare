from django.urls import path
from accounts.views.register_parent import register_parent_view
from accounts.views.register_specialist import register_specialist_view
from accounts.views.login import login_view
from accounts.views.greet import greet_view

app_name = "accounts"

urlpatterns = [
    path("register/parent/", register_parent_view, name="register_parent"),
    path("register/specialist/", register_specialist_view, name="register_specialist"),
    path("login/", login_view, name="login"),
    path("greet/", greet_view, name="greet"),
]
