from django.urls import path
from accounts.views.register_parent import register_parent_view
from accounts.views.register_specialist import register_specialist_view
from accounts.views.login import login_view
from accounts.views.greet import greet_view
from accounts.views.logout import logout_view
from accounts.views.profile import profile_view
from accounts.views.greet import greet_posts_view

app_name = "accounts"

urlpatterns = [
    path("register/parent/", register_parent_view, name="register_parent"),
    path("register/specialist/", register_specialist_view, name="register_specialist"),
    path("login/", login_view, name="login"),
    path("greet/", greet_view, name="greet"),
    path("greet/posts/", greet_posts_view, name="greet-posts"),
    path("profile/", profile_view, name="profile"),
    path("logout/", logout_view, name="logout"),
]
