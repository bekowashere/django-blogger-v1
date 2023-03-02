from django.core.management import BaseCommand, CommandError
from blog.utils import generate_posts


class Command(BaseCommand):
    help = "Generate dummy data for Post model"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        numbers = options["count"]

        try:
            generate_posts(numbers)
            self.stdout.write(self.style.SUCCESS(f"Dummy 'Post' Data create successfully"))
        except Exception as e:
            raise CommandError(f"{e}")
