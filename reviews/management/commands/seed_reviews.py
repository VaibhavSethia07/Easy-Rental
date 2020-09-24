import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from reviews import models as review_models

NAME = "reviews"

class Command(BaseCommand):

    help = "This command create {NAME}."

    def add_arguments(self, parser):

        parser.add_argument("--number", default=1, type=int, help="How many {NAME} you want to create?")

    def handle(self, *args, **options):

        seeder = Seed.seeder()
        number = options.get("number")
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()

        seeder.add_entity(review_models.Review, number, {
            "cleanliness": lambda x: random.randint(1,5),
            "accuracy": lambda x: random.randint(1,5),
            "communication": lambda x: random.randint(1,5),
            "location": lambda x: random.randint(1,5),
            "check_in": lambda x: random.randint(1,5),
            "value": lambda x: random.randint(1,5),
            "user": lambda x: random.choice(all_users),
            "room": lambda x: random.choice(all_rooms),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created")) 

