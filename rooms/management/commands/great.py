from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    help = "This command tells me that you are great!"

    def add_arguments(self, parser):
        
        parser.add_argument("--times", help="How many tmes do you want me to tell you that you are great?",)
        
    def handle(self, *args, **options):
        print(args, options)
        times = options.get("times")

        for t in range(int(times)):
            self.stdout.write(self.style.ERROR("You are great!"))