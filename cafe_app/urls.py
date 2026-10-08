from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("menu/", views.menu, name="menu"),

    path("login/", views.login_page, name="login"),

    path("register/", views.register, name="register"),

    path("reservation/", views.reservation, name="reservation"),

    path("cart/", views.viewcart, name="cart"),
]