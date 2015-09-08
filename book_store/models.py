from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    bio = models.TextField()

    __str__ = lambda self: '%s %s' % (self.name, self.last_name)


class Book(models.Model):
    author = models.ForeignKey(Author,
                               related_name='books',
                               related_query_name='book')
    title = models.CharField(max_length=128)

    __str__ = lambda self: '"%s" by %s' % (self.title, self.author)


class ChapterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .select_related('book') \
            .order_by('book', 'chapter_number')


class Chapter(models.Model):
    book = models.ForeignKey(Book,
                             related_name='chapters',
                             related_query_name='chapter')
    chapter_number = models.PositiveIntegerField()
    title = models.CharField(max_length=128)

    objects = ChapterManager()

    __str__ = lambda self: '"%s", ch. %d: %s' % \
                           (self.book.title, self.chapter_number, self.title)


class PageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .select_related('chapter') \
            .order_by('chapter__chapter_number', 'page_number')


class Page(models.Model):
    chapter = models.ForeignKey(Chapter,
                                related_name='pages',
                                related_query_name='page')
    page_number = models.PositiveIntegerField()
    text = models.TextField()

    objects = PageManager()

    __str__ = lambda self: '"%s", ch. %d, page %s' % \
                           (self.chapter.title,
                            self.chapter.chapter_number,
                            self.page_number)
