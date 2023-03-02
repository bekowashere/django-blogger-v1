import random

from django.contrib.auth.models import User
from django.utils.text import slugify
from faker import Faker

from blog.models import Category, Post

fake = Faker()
# sluglar için slugify bul


def generate_users(num):
    for _ in range(num):
        user = User.objects.create_user(
            username=fake.unique.user_name(),
            password="parola12345",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
        )
        user.save()


def generate_categories(num_categories):
    for _ in range(num_categories):
        title = fake.unique.word()
        slug = slugify(title.lower())
        content = fake.text(max_nb_chars=30)
        Category.objects.create(title=title, slug=slug, content=content)


def generate_posts(num_books):
    for _ in range(num_books):
        title = fake.unique.text(max_nb_chars=128)
        subtitle = fake.text(max_nb_chars=128)
        slug = slugify(title.lower())
        content = fake.sentence(nb_words=20)

        # author
        user_count = User.objects.count()
        user_id = random.randint(1, user_count - 1)
        user = User.objects.get(id=user_id)

        # category
        category_count = Category.objects.count()
        category_id = random.randint(1, category_count - 1)
        category = Category.objects.get(id=user_id)

        status = 1

        Post.objects.create(
            author=user,
            title=title,
            subtitle=subtitle,
            slug=slug,
            content=content,
            category=category,
            status=status,
        )
