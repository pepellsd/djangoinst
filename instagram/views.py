import django.contrib.sites.shortcuts
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import HttpResponse

from .models import Post
from .models import Picture


# def index(request):
#     posts = Post.objects.all()
#     return HttpResponse("main page instagram", posts)


def login(request):
    return HttpResponse("login page")


# def view_post(request, post_id):
#     post = Post.objects.get_object_or_404(pk=post_id)
#     return HttpResponse(f"post id:{post_id}", post)


class PictureListViewMain(ListView):
    model = Picture
    template_name = '../instagram/'
    context_object_name = 'pictures'



