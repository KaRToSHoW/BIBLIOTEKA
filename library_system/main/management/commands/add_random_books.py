import random
from django.core.management.base import BaseCommand
from faker import Faker
from main.models import Book, Genre

class Command(BaseCommand):
    help = "Добавляет случайные книги в базу данных"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=10,
            help='Количество книг для добавления'
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options['count']

        genres = list(Genre.objects.all())
        if not genres:
            self.stdout.write(self.style.ERROR("Сначала добавьте жанры в базу данных."))
            return

        books = []
        for _ in range(count):
            book = Book(
                title=fake.sentence(nb_words=4),
                author=fake.name(),
                publisher=fake.company(),
                description=fake.text(max_nb_chars=200),
                published_date=fake.date_this_century(),
            )
            book.save()
            book.genres.set(random.sample(genres, k=min(3, len(genres))))  # До 3 жанров на книгу
            books.append(book)

        self.stdout.write(self.style.SUCCESS(f"Успешно добавлено {len(books)} книг."))
