from django.urls import path
from .views import register, login_view, logout_view, PersonalInfo, user_Payments

urlpatterns = [
    path("login/", login_view, name="user_login"),
    path("register/", register, name="user_register"),
    path("logout/", logout_view, name="user_logout"),
    path("User/<int:user_id>", PersonalInfo, name="user_info"),
    path("user_Payments/<int:user_id>", user_Payments, name="user_Payments"),

]
