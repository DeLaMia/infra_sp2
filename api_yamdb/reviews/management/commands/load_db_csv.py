from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

LOAD_ERROR = """DELETE db.qlite3 and repeat"""


class Command(BaseCommand):
    help = "load from csv"

    def handle(self, *args, **options):
        if (Title.objects.exists()
                or Genre.objects.exists()
                or Category.objects.exists()
                or GenreTitle.objects.exists()
                or User.objects.exists()
                or Review.objects.exists()
                or Comment.objects.exists()):
            print("already loaded")
            print(LOAD_ERROR)
            return

        print("loading...")
        print('categories')
        for row in DictReader(open('static/data/category.csv',
                                   encoding='utf8')):
            category = Category(id=row['id'], name=row['name'],
                                slug=row['slug'])
            category.save()
        print('title')
        for row in DictReader(open('static/data/titles.csv', encoding='utf8')):
            title = Title(id=row['id'], name=row['name'], year=row['year'],
                          category=Category.objects.get(id=row['category']))
            title.save()
        print('user')
        for row in DictReader(open('static/data/users.csv', encoding='utf8')):
            user = User(id=row['id'], username=row['username'],
                        email=row['email'], role=row['role'])
            user.save()
        print('rewiew')
        for row in DictReader(open('static/data/review.csv', encoding='utf8')):
            review = Review(id=row['id'], title_id=row['title_id'],
                            text=row['text'],
                            author=User.objects.get(id=row['author']),
                            score=row['score'], pub_date=row['pub_date'])
            review.save()
        print('com')
        for row in DictReader(open('static/data/comments.csv',
                                   encoding='utf8')):
            comment = Comment(
                id=row['id'],
                review_id=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date'])
            comment.save()
        print('genre')
        for row in DictReader(open('static/data/genre.csv', encoding='utf8')):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()
        print('gentit')
        for row in DictReader(open('static/data/genre_title.csv',
                                   encoding='utf8')):
            genre_title = GenreTitle(id=row['id'],
                                     title_id=row['title_id'],
                                     genre_id=row['genre_id'])
            genre_title.save()
        print('OK')
