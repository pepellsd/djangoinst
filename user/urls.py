from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('register/', Registration.as_view(), name="register"),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('edit_profile/', ProfileEdit.as_view(), name="edit_profile"),
    path('upload_images/', UploadImagesUser.as_view(), name="upload_images")
]