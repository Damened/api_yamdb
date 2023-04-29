import csv
from api_yamdb.api_yamdb.reviews.

class

    def handle(self, *args, **options):
        with open('names.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['id'], row['name'])
                record = Category(**kwargs)