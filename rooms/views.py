from math import ceil
from datetime import datetime
from django.shortcuts import render
from . import models

def all_rooms(request):
    page = int(request.GET.get("page",1))
    page_size = 10
    limit = page * page_size
    offset = limit - page_size
    rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    
    return render(request, "rooms/home.html", {
        "room": rooms,
        "page": page,
        "page_count": page_count,
        "page_range": range(1,page_count+1)
        
    })
    
    
    
    
    
