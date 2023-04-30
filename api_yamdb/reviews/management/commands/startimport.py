import csv
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from reviews.models import Category


PATH = f'{settings.BASE_DIR}/static/data/'


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(PATH + 'category.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            records = []
            for row in reader:
                records.append(Category(**row))
        Category.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS('Данные импортированы.'))