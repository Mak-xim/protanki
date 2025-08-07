from django.urls import path
from .views import register_view, login_view, logout_view
from .views import activate_account
# from django.contrib.auth.views import LogoutView

# class MyLogoutView(LogoutView):
#     def post(self, request, *args, **kwargs):
#         return self.logout(request, *args, **kwargs)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
]