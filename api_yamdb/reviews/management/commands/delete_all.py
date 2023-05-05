from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class Command(BaseCommand):
    help = "delete all models data from db"

    def handle(self, *args, **options):
        Title.objects.all().delete()
        Category.objects.all().delete()
        GenreTitle.objects.all().delete()
        Genre.objects.all().delete()
        User.objects.all().delete()
        Review.objects.all().delete()
        Comment.objects.all().delete()
        print('all data deleted')
