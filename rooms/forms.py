from django import forms
from django.forms import ModelForm
from django_countries.fields import CountryField
from . import models

class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="IN").formfield()
    price = forms.IntegerField(required=False, min_value=0)
    room_type = forms.ModelChoiceField(required=False, empty_label="Any kind", queryset=models.RoomType.objects.all())
    guests = forms.IntegerField(required=False, min_value=1)
    beds = forms.IntegerField(required=False, min_value=1)
    bedrooms = forms.IntegerField(required=False, min_value=1)
    baths = forms.IntegerField(required=False, min_value=1)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class CreatePhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = ("caption", "file")
        
    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        models.Room.objects.get(pk=pk)
        print(pk)

