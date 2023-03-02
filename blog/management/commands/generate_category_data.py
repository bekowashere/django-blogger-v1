from django.core.management import BaseCommand, CommandError
from blog.utils import generate_categories

class Command(BaseCommand):
    help = "Generate dummy data for 'Category' model"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        numbers = options["count"]

        try:
            generate_categories(numbers)
            self.stdout.write(self.style.SUCCESS(f"Dummy 'Category' Data create successfully"))
        except Exception as e:
            raise CommandError(f"{e}")
