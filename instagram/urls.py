from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('posts/<int:pk>', ViewPost.as_view(), name="view_post"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('posts/<int:post_id>/delete/', DeletePost.as_view(), name="delete_post"),
    path('posts/<int:post_id>/comment', LeaveComment.as_view(), name="leave_comment"),
    path('posts/<int:post_id>/like_unlike', LikeUnlike.as_view(), name="like_unlike"),
    path('create_post/', CreatePost.as_view(), name="create_post"),
]