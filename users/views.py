import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms, models

class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": ""}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)
    
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))

class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Vaibhav",
        "last_name": "Sethia",
        "email": "vaibhavsethia110@gmail.com"
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success messsage
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))

def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "http://127.0.0.1:8001/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )

class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"}
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                # print(profile_request.json())
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    if email is None:
                        raise GithubException() 
                    bio = profile_json.get("bio")
                    avatar_url = profile_json.get("avatar_url")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                        if avatar_url is not None:
                            photo_request = requests.get(avatar_url)
                            user.avatar.save(f"{username}-avatar", ContentFile(photo_request.content)
                        )
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))








# class LoginView(View):
# 
    # def get(self, request):
        # form = forms.LoginForm(initial={"email": "vaibhavsethia110@gmail.com"})
        # return render(request, "users/login.html", {"form": form})
        # 
# 
    # def post(self, request):
        # form = forms.LoginForm(request.POST)
        # 
        # if form.is_valid():
            # email = form.cleaned_data.get("email")
            # password = form.cleaned_data.get("password")
# 
            # user = authenticate(request, username=email, password=password)
            # if user is not None:
                # login(request, user)
                # return redirect(reverse("core:home")) 
        # return render(request, "users/login.html", {"form": form})
        
# def log_out(request):
    # logout(request)
    # return redirect(reverse("core:home"))