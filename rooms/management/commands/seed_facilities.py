from django.core.management.base import BaseCommand
from rooms.models import Facility

NAME = "facilities"

class Command(BaseCommand):

    help = "This command create {NAME}."

    def handle(self, *args, **options):

        facilities = [
            "Free parking on premises",

            "Gym",

            "Hot tub",

            "Pool",
        ]

        for facility in facilities:

        Facility.objects.create(name=facility)
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} {NAME} created"))

