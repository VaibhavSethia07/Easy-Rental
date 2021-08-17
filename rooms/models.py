from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
from core import models as core_models
from cal import Calendar
import re

class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item Definition """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    
    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ Room Type Model Definition """

    subtitle = models.CharField(max_length=140, null=True)

    class Meta:
        verbose_name = "Room Type"

class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"

class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"

class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"

class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """
    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to = "room_photos")
    room = models.ForeignKey("Room",related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):


    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    beds = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    bedrooms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    baths = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey("users.User", related_name="rooms", on_delete=models.CASCADE)
    room_type = models.ForeignKey("RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name
    
    def capitalizer(self, model_field, delimiter):
        
        parts = model_field.split(delimiter)
        for part in range(len(parts)):
            parts[part] = str.capitalize(parts[part])
        model_field = delimiter.join(parts)
        return model_field

    def save(self, *args, **kwargs):

        self.name = self.capitalizer(self.name, " ")
        self.description = self.capitalizer(self.description, ". ")
        self.city = self.capitalizer(self.city, " ")
        self.address = self.capitalizer(self.address, " ")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        
        if(len(all_reviews)>0):
            for review in all_reviews:
                all_ratings += review.rating_average()
            
            return round(all_ratings / len(all_reviews),2)
        return 0

    def first_photo(self):
        try:
            photo, = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def count_reviews(self):
        all_reviews = self.reviews.all()
        return len(all_reviews)

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1

        month_list_cal = []

        for i in range(0, 3):
            month_list_cal.append(Calendar(this_year, (this_month + i-1) % 12+1))
            
            if ((this_month + i) % 12 == 0):
                this_year+=1

        return month_list_cal

