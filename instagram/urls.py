from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('posts/<int:post_id>', view_post, name="view_post"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('register/', Registration.as_view(), name="register"),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('edit_profile', ProfileEdit.as_view(), name="edit_profile"),
    path('posts/<int:post_id>/delete/', delete_post, name="delete_post"),
    path('posts/<int:post_id>/comment', leave_comment, name="leave_comment"),
    path('posts/<int:post_id>/like_unlike', like_unlike_post, name="like_unlike")
]