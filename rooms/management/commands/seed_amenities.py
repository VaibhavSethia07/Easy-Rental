from django.core.management.base import BaseCommand
from rooms.models import Amenity

NAME  = "amenities"

class Command(BaseCommand):
    
    help = "This command create {NAME}."
        
    def handle(self, *args, **options):
        
        amenities = [
            "Kitchen",                       
            "Shampoo",            
            "Heating",            
            "Air conditioning",            
            "Washing machine",            
            "Dryer",            
            "Wifi",            
            "Breakfast",            
            "Indoor fireplace",            
            "Hangers",            
            "Iron",            
            "Hair dryer",            
            "Laptop-friendly workspace",            
            "TV",            
            "Cot",            
            "High chair",            
            "Self check-in",            
            "Smoke alarm",            
            "Carbon monoxide alarm",            
            "Private bathroom",            
            "Piano",            
            "Beachfront",            
            "Waterfront",            
            "Ski-in/Ski-out",
        ]

        for amenity in amenities:
            Amenity.objects.create(name=amenity)

        self.stdout.write(self.style.SUCCESS(f"{len(amenities)} {NAME} created!"))
        

        
        