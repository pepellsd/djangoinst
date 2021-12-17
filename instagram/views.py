import django.contrib.sites.shortcuts
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.template.context import RequestContext

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView

from django.shortcuts import HttpResponse

from .models import Post
from .models import Picture


def index(request):
    posts = Post.objects.all()
    return render(request, "index.html", {"posts": posts})


def login(request):
    return HttpResponse("login page")


def view_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, "post.html", {"post": post})


# class PostView(TemplateView):
#     model = Post
#     template_name = 'post.html'
#     context_object_name = 'post'



# class PostTagListViewMain(PostListViewMain):
#     template_name =



# Просмотр постов, профиля только для авторизованных пользователей
#
# Страничка профиля юзера и постами
#
# Регистрация по емейл
#
# Логин
#
# Фронт
#
# Отображение одного поста
#
# Поиск по тегам



