from django.core.management import BaseCommand, CommandError
from blog.utils import generate_users


class Command(BaseCommand):
    help = "Generate dummy data for User model"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        numbers = options["count"]

        try:
            generate_users(numbers)
            self.stdout.write(self.style.SUCCESS(f"Dummy 'User' Data create successfully"))
        except Exception as e:
            raise CommandError(f"{e}")
