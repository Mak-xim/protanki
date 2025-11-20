from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, change_password
from .views import activate_account, send_password_reset
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth import views as auth_views
# from .views import AutoPasswordResetView


# class MyLogoutView(LogoutView):
#     def post(self, request, *args, **kwargs):
#         return self.logout(request, *args, **kwargs)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),

    path('send-password-reset/', send_password_reset, name='send_password_reset'),
    path('change_password/', change_password,  name='change_password'),

    path("password_reset/",
         auth_views.PasswordResetView.as_view(),
         name="password_reset"),

    path("password_reset/done/",
         auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),

    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]