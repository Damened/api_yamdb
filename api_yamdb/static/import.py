import sys
from ..reviews.models import Category


def import_category():
    category = open('data/category.csv', 'r')
    ids = []
    names = []
    slugs = []
    for line in category:
        ids.append(line.split('\n')[0].split(',')[0])
        names.append(line.split('\n')[0].split(',')[1])
        slugs.append(line.split('\n')[0].split(',')[2])
    for i in range(1, len(ids)):
        Category.objects.create(id=ids[i], name=names[i], slug=slugs[i])
        print(ids[i], names[i], slugs[i])


def main():
    import_category()
    #import_comments()
    #import_genre()
    #import_genre_title()
    #import_review()
    #import_titles()
    #import_users()


if __name__ == "__main__":
    main()