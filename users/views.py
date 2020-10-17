import os
import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models

class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "vaibhavsethia110@gmail.com"}

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
    redirect_uri = ""
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")

def github_callback(request): 
    client_id = os.environ.get("GITHUB_ID")
    client_secret = os.environ.get("GITHUB_SECRET")
    code = request.GET.get("code", None)
    if code is not None:
        request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"}
        )
        result_json = request.json()
        error = result_json.get("error", None)
        if error is not None:
            return redirect(reverse("users:login"))
        else:
            access_token = result_json.get("access_token")
            profile_request = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json",
                },
            )
            profile_json = profile_request.json()
            username = profile_json.get("login", None)
            if username is not None:
                name = profile_json.get("name")
                email = profiel_json.get("email")
                bio = profile_json.get("bio")
                models.User.objects.get(email=email)
                if user is not None:
                    return redirect(reverse("users:login"))
                else:
                    user = models.User.objects.create(
                    username=email,
                    first_name=first_name, 
                    bio=bio, 
                    email=email,
                )
                login(request, user)
                return redirect(reverse("core:home"))
            else:
                return redirect(reverse("users:login"))
    else:
        return redirect(reverse("core:home"))









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