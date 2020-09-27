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

    city_parts = city.split(" ")
    for part in range(len(city_parts)):
        city_parts[part] = str.capitalize(city_parts[part])
    city = " ".join(city_parts)

    room_types = models.RoomType.objects.all()

    form = {"city": city, "countries": countries, "room_types": room_types,}
    
    choices = {"s_room_type": room_type, "s_country": country, }

    return render(request,"rooms/search.html", { **form, **choices})



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
    
    
    
    
    
