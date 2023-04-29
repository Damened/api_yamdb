import csv
from django.core.management.base import BaseCommand, CommandError
from api_yamdb.api_yamdb.api_yamdb import settings
from api_yamdb.api_yamdb.reviews.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/static/data/category.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            records = []
            for row in reader:
                print(row)
                record = Category(**row)
                records.append(record)
        Category.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS('Данные импортированы.'))
