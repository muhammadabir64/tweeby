from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import profile, register, login_page, logout_page, follow_handler, nav_search_bar, following_list, followers_list, follower_remover, following_remover, profile_edit, account_setting_email, account_setting_password


urlpatterns = [
    path("u/<str:username>/", profile, name="profile"),
    path("register/", register, name="register"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("follow_handler/", follow_handler, name="follow_handler"),
    path("nav_search_bar/", nav_search_bar, name="nav_search_bar"),
    path("following_list/", following_list, name="following_list"),
    path("followers_list/", followers_list, name="followers_list"),
    path("follower_remover/", follower_remover, name="follower_remover"),
    path("following_remover/", following_remover, name="following_remover"),
    path("profile_edit/", profile_edit, name="profile_edit"),
    path("account_setting_email/", account_setting_email, name="account_setting_email"),
    path("account_setting_password/", account_setting_password, name="account_setting_password"),

    path("password_reset/", PasswordResetView.as_view(template_name="account/password_reset.html", html_email_template_name="account/password_mail.html"), name="password_reset"),
    path("password_reset_done/",PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset_complete/", PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name="password_reset_complete")
]