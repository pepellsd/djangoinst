import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.utils import timezone

from instagram.models import Picture
from .models import User, Token
from .forms import UserRegisterForm, UserEditForm, UploadUserImagesForm, UserLoginForm


class LoginUser(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        form = UserLoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse("form fill incorrect ")
        email = form.data.get("email")
        password = form.data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("no user with this email")
        if authenticate(email=email, password=password):
            login(request, user)
            return redirect("index")
        return HttpResponse("password not correct")


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
            token = Token(code=self.gen_token._make_token_with_timestamp(user=user, timestamp=60 * 60 * 24),
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
            return HttpResponse("confirm email address")
        else:
            return render(request, "reg.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return HttpResponse("activation failed user not exist", status=401)
    _token = Token.objects.filter(user_id=user.pk).first()
    if user and _token and token == _token.code and _token.expiration_date >= timezone.now():
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("profile")
    else:
        return HttpResponse("activation failed expiration date left", status=401)


class ProfileEdit(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, "update_profile.html", {"form": form})

    def post(self, request):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("form fill incorrect")
        return redirect("profile")


class UploadImagesUser(LoginRequiredMixin, View):
    form = UploadUserImagesForm()

    def get(self, request):
        return render(request, "upload_images.html", context={"form": self.form})

    def post(self, request, *args, **kwargs):
        form = UploadUserImagesForm(request.FILES)
        if not form.is_valid():
            return render(request, "upload_images.html", {"form": form})
        user = User.objects.get(id=request.user.pk)
        files = request.FILES.getlist('images')
        for file in files:
            picture = Picture(path=file)
            picture.save()
            user.images.add(picture)
        return redirect("profile")
