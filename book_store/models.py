from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    bio = models.TextField()


class Book(models.Model):
    author = models.ForeignKey(Author,
                               related_name='books',
                               related_query_name='book')
    title = models.CharField(max_length=128)


class Chapter(models.Model):
    book = models.ForeignKey(Book,
                             related_name='chapters',
                             related_query_name='chapter')
    chapter_number = models.PositiveIntegerField()
    title = models.CharField(max_length=128)


class Page(models.Model):
    chapter = models.ForeignKey(Chapter,
                                related_name='pages',
                                related_query_name='page')
    page_number = models.PositiveIntegerField()
    text = models.TextField()
