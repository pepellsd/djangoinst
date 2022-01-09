from django.views.generic import View, DetailView, ListView
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError

from .models import Post, Like, Comment, Picture
from .forms import CreatePostForm, CommentForm


class Index(ListView, LoginRequiredMixin):
    model = Post
    template_name = "index.html"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            posts = Post.objects.get_queryset().filter(tags__name=search).exclude(
                user_id=self.request.user.id).order_by('id')
        else:
            posts = Post.objects.get_queryset().exclude(user_id=self.request.user.id).order_by('id')
        return posts


class ViewPost(DetailView, LoginRequiredMixin):
    model = Post
    template_name = "post.html"


class ProfileView(View, LoginRequiredMixin):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user_id=user.pk)
        return render(request, "profile.html", {"user": user, "posts": posts})


class DeletePost(View, LoginRequiredMixin):
    def post(self, request, post_id):
        user_pk = request.user.pk
        post = Post.objects.get(pk=post_id)
        if post.user_id != user_pk:
            return HttpResponse("it's not your post", status=406)
        Post.delete(post)
        return redirect("profile")


class LeaveComment(View, LoginRequiredMixin):
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if not form.is_valid():
            return HttpResponse("form is fill incorrect ")
        user_pk = request.user.pk
        comment_text = request.POST["comment_text"]
        comment = Comment(user_id=user_pk, post_id=post_id, text=comment_text)
        comment.save()
        return redirect("view_post", post_id)


class LikeUnlike(View, LoginRequiredMixin):
    def post(self, request, post_id):
        user_pk = request.user.pk
        like = Like.objects.filter(user_id=user_pk, post_id=post_id).delete()
        if like[0] == 0:
            like = Like(user_id=user_pk, post_id=post_id)
            like.save()
        return redirect("view_post", post_id)


class CreatePost(View, LoginRequiredMixin):
    def get(self, request):
        form = CreatePostForm()
        return render(request, "create_post.html", context={"form": form})

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if not form.is_valid():
            return HttpResponse("form is fill incorrect")
        files = request.FILES.getlist('images')
        post = Post(user=request.user, description=request.POST["description"])
        post.save()
        try:
            tags = request.POST["tags"]
            post.tags.set(tags)
        except MultiValueDictKeyError:
            pass
        for file in files:
            picture = Picture(path=file)
            picture.save()
            post.images.add(picture)
        return redirect("view_post", pk=post.pk)
