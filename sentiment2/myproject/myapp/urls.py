from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path("signup/", views.signup_view, name="signup"),
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Home URL (protected)
    path("home/", views.home, name="home"),

]




