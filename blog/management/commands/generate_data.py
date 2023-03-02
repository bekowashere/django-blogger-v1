from django.core.management import BaseCommand, CommandError
from blog.utils import generate_categories, generate_posts, generate_users


class Command(BaseCommand):
    help = "Generate dummy data for 'blog' app include User, Category and Post models"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        numbers = options["count"]

        try:
            generate_users(numbers)
            self.stdout.write(
                self.style.WARNING(f"Users Dummy Data create successfully")
            )
            generate_categories(numbers)
            self.stdout.write(
                self.style.WARNING(f"Category Dummy Data create successfully")
            )
            generate_posts(numbers)
            self.stdout.write(
                self.style.WARNING(f"Post Dummy Data create successfully")
            )

            self.stdout.write(self.style.SUCCESS(f"Dummy Data create successfully"))
        except Exception as e:
            raise CommandError(f"{e}")
