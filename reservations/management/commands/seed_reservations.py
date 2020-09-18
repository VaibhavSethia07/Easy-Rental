import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from django.utils import timezone
from reservations  import models as reservation_models
from users import models as user_models
from rooms import models as room_models
from datetime import timedelta

NAME = "reservations"

class Command(BaseCommand):

    help = "This command creates reservations."

    def add_arguments(self, parser):

        parser.add_argument("--number", default=1, type=int, help="How many {NAME} you want to create?")

    def handle(self, *args, **options):
        
        seeder = Seed.seeder()
        number = options.get("number")
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        seeder.add_entity(reservation_models.Reservation, number, {
            "status": lambda x: random.choice(["pending", "canceled", "confirmed"]),
            "guest" : lambda x: random.choice(all_users),
            "room" : lambda x: random.choice(all_rooms),
            "check_in" : timezone.now(),
            "check_out" : timezone.now() + timedelta(days=random.randint(3,25)) 
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
