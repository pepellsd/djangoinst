from django.urls import path


from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('login/', login, name="login"),
    path('posts/<int:post_id>', view_post, name="view_post")
]