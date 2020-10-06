from django.contrib.auth.models import AbstractUser
from django.db import models


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
    email_confirmed = models.BooleanField(default=False)
    email_secret = models.BooleanField(max_length=120, default="")

    def verify_email(self):
        pass

    
    
