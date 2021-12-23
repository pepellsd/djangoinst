import datetime

from django.views.generic import View
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, User, Like, Comment, Token
from .forms import UserRegisterForm, UserEditForm


@login_required()
def index(request):
    search = request.GET.get("search")
    if search:
        posts = Post.objects.exclude(user_id=request.user.id, tags__name=search)
    else:
        posts = Post.objects.exclude(user_id=request.user.id)
    return render(request, "index.html", {"posts": posts})


@login_required()
def view_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post_id=post.id).all()
    len_likes = len(Like.objects.filter(post_id=post.id).all())
    return render(request, "post.html", {"post": post, "comments": comments, "likes_count": len_likes})


class LoginUser(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("no user with this email")
        if authenticate(email=email, password=password):
            login(request, user)
            return redirect("index")
        return HttpResponse("password not correct")


class ProfileView(View, LoginRequiredMixin):
    def get(self, request):
        user = request.user
        posts = Post.objects.filter(user_id=user.pk)
        return render(request, "profile.html", {"user": user, "posts": posts})


class ProfileEdit(View, LoginRequiredMixin):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, "update_profile.html", {"form": form})

    def post(self, request):
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
        else:
            return HttpResponse("форма не правильно заполнена")
        return redirect("profile")


@login_required()
def delete_post(request):
    pass


@login_required()
def leave_comment(request):
    pass


class Registration(View):
    gen_token = PasswordResetTokenGenerator()

    def get(self, request):
        form = UserRegisterForm()
        return render(request, "reg.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            token = Token(code=self.gen_token._make_token_with_timestamp(user=user, timestamp=60*60*24),
                          user_id=user.pk,
                          expiration_date=datetime.datetime.now() + datetime.timedelta(days=1))
            token.save()
            email_sub = "activate account"
            msg = render_to_string("activate.html", {
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token.code
            })
            email = EmailMessage(email_sub, msg, settings.EMAIL_HOST_USER, [user.email])
            email.send()
            return HttpResponse("подтвердите почту")
        else:
            return HttpResponse("форма не правильно заполнена")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user=None
    _token = Token.objects.filter(user_id=user.pk).first()
    if user and token==_token.code:
        if _token.expiration_date >= timezone.now():
            user.is_active =True
            user.save()
            login(request, user)
            return redirect("profile")
    else:
        return HttpResponse("activation failed", status=401)