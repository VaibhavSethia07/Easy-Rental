from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

NAME = "users"

class Command(BaseCommand):
    
    help = "This command creates {NAME}."

    def add_arguments(self, parser):
        
        parser.add_argument("--number", default=2, type=int, help="How many {NAME} you want to create?",)
        
    def handle(self, *args, **options):

        seeder = Seed.seeder()
        number = options.get("number")
        seeder.add_entity(User, number, { "is_staff" : False, "is_superuser" : False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
        

        
        