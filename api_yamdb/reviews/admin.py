from django.contrib import admin
from .models import Title, Review, Comment, Category, Genre

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', )
    search_fields = ('pk', 'name', 'slug', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', )
    search_fields = ('pk', 'name', 'slug', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category', )
    search_fields = ('pk', 'name', 'year', 'description', 'category', )
    list_filter = ('category', )
    empty_value_display = '-пусто-'
    list_editable = ('category', )
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'review', 'pub_date',)
    search_fields = ('pk', 'author', 'text', 'review', 'pub_date',)
    list_filter = ('review', )


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'score', 'pub_date',)
    search_fields = ('pk', 'author', 'title', 'text', 'score', 'pub_date',)


admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)