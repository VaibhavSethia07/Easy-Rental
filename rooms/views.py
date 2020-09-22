from math import ceil
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models

def all_rooms(request):
    page = request.GET.get("page",1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10,orphans=5)

    try:
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", { "page": rooms,})

    except EmptyPage:
        return redirect("/",)

    

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
    
    
    
    
    
