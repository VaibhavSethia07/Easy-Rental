from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import uuid


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_GOOGLE = "google"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_GOOGLE, "Google"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_HINDI = "hi"  # LANGUAGE_KOREAN = "krw"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_HINDI, "Hindi"),  # (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_INR = "inr"  # CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_INR, "INR"),  # (CURRENCY_KRW, "KRW"),
    )

    avatar = models.ImageField( blank=True, upload_to="avatars")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField (blank=True, null=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_ENGLISH)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_INR)
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default = LOGIN_EMAIL)

    def verify_email(self):
        
        if self.email_verified is True:
            return;

        secret = uuid.uuid4().hex[:20]
        self.email_secret = secret
        html_message = render_to_string("emails/verify_email.html", context={"secret": secret})
        send_mail(
            "Verify Easy Rental Account",
            strip_tags(html_message),
            settings.EMAIL_FROM,
            [self.email],
            fail_silently=False,
            html_message=html_message
        )
        self.save()


    
    
