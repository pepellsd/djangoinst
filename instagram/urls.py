from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('posts/<int:post_id>', view_post, name="view_post"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('register/', Registration.as_view(), name="register"),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]