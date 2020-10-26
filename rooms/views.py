from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView,UpdateView, View
from django.core.paginator import Paginator
from users import mixins as user_mixins
from django_countries import countries
from . import models, forms


class HomeView(ListView):

    """ HomeView Definiton """
    model = models.Room
    ordering = "created"
    paginate_by = 12
    paginate_orphans = 5
    context_object_name = "rooms"

# Class based view of rooms 
class RoomDetail(DetailView):
    
    """ RoomDetail Definition """
    model = models.Room

class SearchView(View):

    def get(self, request):
        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                price = form.cleaned_data.get("price")
                room_type = form.cleaned_data.get("room_type")
                guests = form.cleaned_data.get("guests")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if instant_book:
                    filter_args["instant_book"] = True

                if superhost:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(object_list=qs, per_page=10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(request, "rooms/search.html", {"form": form, "rooms": rooms})

        else:

            form =  forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form,})

class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = {
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "room_type",
        "amenities",
        "facilities",
        "house_rules"
    }

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "room_photos.html"
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room




























    # city = request.GET.get("city", "Anywhere")
    # country = request.GET.get("country","IN")
    # room_type = int(request.GET.get("room_type", 0))
    # price = int(request.GET.get("price",0))
    # guests = int(request.GET.get("guests",0))
    # beds = int(request.GET.get("beds",0))
    # bedrooms = int(request.GET.get("bedrooms",0))
    # baths = int(request.GET.get("baths", 0))
    # instant = bool(request.GET.get("instant", False))
    # superhost = bool(request.GET.get("superhost", False))
    # s_amenities = request.GET.getlist("amenities")
    # s_facilities = request.GET.getlist("facilities")
    
    

    # city_parts = city.split(" ")
    # for part in range(len(city_parts)):
    #     city_parts[part] = str.capitalize(city_parts[part])
    # city = " ".join(city_parts)

    # form = {
    #     "city": city,
    #     "s_room_type": room_type,
    #     "s_country": country,
    #     "price": price,
    #     "guests": guests,
    #     "beds": beds,
    #     "bedrooms": bedrooms,
    #     "baths": baths,
    #     "s_amenities" : s_amenities,
    #     "s_facilities": s_facilities,
    #     "instant": instant,
    #     "superhost": superhost,
    # }

    # room_types = models.RoomType.objects.all()
    # amenities = models.Amenity.objects.all()
    # facilities = models.Facility.objects.all()

    # choices = {
    #     "countries": countries,
    #     "room_types": room_types,
    #     "amenities": amenities,
    #     "facilities": facilities,
    # }

    # filter_args = {}

    # if city != "Anywhere":
    #     filter_args["city__startswith"] = city
    
    # filter_args["country"] = country

    # if room_type != 0:
    #     filter_args["room_type__pk"] = room_type

    # if price != 0:
    #     filter_args["price__lte"] = price
    
    # if guests != 0:
    #     filter_args["guests__gte"] = guests

    # if beds != 0:
    #     filter_args["beds__gte"] = beds

    # if bedrooms != 0:
    #     filter_args["bedrooms__gte"] = bedrooms
    
    # if baths != 0:
    #     filter_args["baths__gte"] = baths
    
    # if instant:
    #     filter_args["instant_book"] = True
    
    # if superhost:
    #     filter_args["host__superhost"] = True

    # if len(s_amenities) > 0:
    #     for s_amenity in s_amenities:
    #         filter_args["amenities__pk"] = int(s_amenity)
        
    # if len(s_facilities) > 0:
    #     for s_facility in s_facilities:
    #         filter_args["facilities__pk"] = int(s_facility)

    # rooms = models.Room.objects.filter(**filter_args)

    # return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
    



# Function based view of rooms
# To use it rename room_detail.html -> detail.html   
# def room_detail(request, pk):
# 
    # try:
        # room = models.Room.objects.get(pk=pk)
        # return render(request, "rooms/detail.html", { "room": room, })
    # except models.Room.DoesNotExist:
        # raise Http404()


# from math import ceil
# from datetime import datetime
# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
# from . import models

# def all_rooms(request):
#     page = request.GET.get("page",1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10,orphans=5)

#     try:
#         rooms = paginator.page(int(page))
#         return render(request, "rooms/home.html", { "page": rooms,})

#     except EmptyPage:
#         return redirect("/",)

    

# def all_rooms(request):
    # page = int(request.GET.get("page",1))
    # page_size = 10
    # limit = page * page_size
    # offset = limit - page_size
    # rooms = models.Room.objects.all()[offset:limit]
    # page_count = ceil(models.Room.objects.count() / page_size)
    # 
    # return render(request, "rooms/home.html", {
        # "room": rooms,
        # "page": page,
        # "page_count": page_count,
        # "page_range": range(1,page_count+1)
        # 
    # })
    
    
    
    
    
