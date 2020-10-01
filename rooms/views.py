from django.shortcuts import render
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django_countries import countries

from . import models


class HomeView(ListView):

    """ HomeView Definiton """
    model = models.Room
    ordering = "created"
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"

# Class based view of rooms 
class RoomDetail(DetailView):
    
    """ RoomDetail Definition """
    model = models.Room

def search(request):

    city = request.GET.get("city", "Anywhere")
    country = request.GET.get("country","IN")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price",0))
    guests = int(request.GET.get("guests",0))
    beds = int(request.GET.get("beds",0))
    bedrooms = int(request.GET.get("bedrooms",0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    
    

    city_parts = city.split(" ")
    for part in range(len(city_parts)):
        city_parts[part] = str.capitalize(city_parts[part])
    city = " ".join(city_parts)

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "beds": beds,
        "bedrooms": bedrooms,
        "baths": baths,
        "s_amenities" : s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city
    
    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if price != 0:
        filter_args["price__lte"] = price
    
    if guests != 0:
        filter_args["guests__gte"] = guests

    if beds != 0:
        filter_args["beds__gte"] = beds

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    
    if baths != 0:
        filter_args["baths__gte"] = baths
    
    if instant:
        filter_args["instant_book"] = True
    
    if superhost:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)
        
    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)
    
    print(s_amenities, s_facilities)

    rooms = models.Room.objects.filter(**filter_args)

    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
    



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
    
    
    
    
    
