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
from django.contrib.auth import login
from django.utils import timezone

from .models import Post, User, Like, Comment, Token
from .forms import UserRegisterForm


def index(request):
    search = request.GET.get("search")
    if search:
        posts = Post.objects.filter(tags__name=search)
        # posts = Post.objects.exclude(user_id=request.user.id, tags__name=search)
    else:
        posts = Post.objects.all()
        # posts = Post.objects.exclude(user_id=request.user.id)

    # Просмотр постов только для авторизованных пользователей
    # Поиск по тегам +
    # посты только других пользователей +
    return render(request, "index.html", {"posts": posts})


def view_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post_id=post.id).all()
    len_likes = len(Like.objects.filter(post_id=post.id).all())
    return render(request, "post.html", {"post": post, "comments": comments, "likes_count": len_likes})


# class PostView(DetailView):
#     template_name = "post.html"
#     model = Post
#     context_object_name = "post"
#     extra_context = {"likes": len(Like.objects.filter(post_id=))}


# Страничка профиля юзера
# просмотр только для авторизованнфх пользователей
class ProfileView(View):
    def get(self, request):
        user = request.user
        return render(request, "profile.html", {"user": user})

    def post(self):
        pass

    def put(self):
        User.objects.get()


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
        print(uid)
        user = User.objects.get(pk=uid)
        print(user)
    except User.DoesNotExist:
        print(f"no user with id {uid}")
        user=None
    print("start checking")
    _token = Token.objects.filter(user_id=user.pk).first()
    if user and token==_token.code:
        print("user and token")
        if _token.expiration_date >= timezone.now():
            print("exp delta")
            user.is_active =True
            user.save()
            login(request, user)
            print("done")
            return redirect("profile")
    else:
        return HttpResponse("activation failed", status=401)