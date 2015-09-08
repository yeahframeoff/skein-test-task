from django.contrib import admin

from .models import Book, Chapter, Author, Page

admin.site.register((Book, Chapter, Author, Page))
