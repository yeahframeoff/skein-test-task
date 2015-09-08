import re
from collections import namedtuple

from . import celery_app
from book_store.models import Book, Page

SearchResultItem = namedtuple('SearchResultItem',
                              ('book_title', 'chapters', 'author'))


def writeline(writer, text, *args, **kwargs):
    return writer.write(text + '\n', *args, **kwargs)


def decompose_query(query):
    words = re.split('\W+', query)
    seen = set()
    return [x.lower() for x in words
            if x.lower() not in seen and
            not seen.add(x.lower())
            ]


def fetch_books(query_parts):
    from django.db.models import Q, Prefetch
    def fetch(query_cond):
        books = Book.objects \
            .select_related('author') \
            .prefetch_related(
            Prefetch('chapters__pages',
                     queryset=Page.objects.filter(query_cond))
        ).all()
        return list(books)

    try:
        query_cond = Q()
        for word in query_parts:
            query_cond |= Q(text__search=word)
        return fetch(query_cond)
    except NotImplementedError:  # for sqlite support
        query_cond = Q()
        for word in query_parts:
            query_cond |= Q(text__icontains=word)
        return fetch(query_cond)


def digest_searchresult(books):
    result = []
    for book in books:
        print(dir(book.chapters))
        item = SearchResultItem(
            book_title=book.title,
            chapters=', '.join(
                '%d (pages %s)' % (ch.chapter_number,
                                   ', '.join(str(p.page_number)
                                             for p in ch.pages.all())
                                   )
                for ch in book.chapters.all()
            ),
            author=book.author
        )
        result.append(item)
    return result


def make_email(search_result, time, original_query):
    from io import StringIO
    from functools import partial
    subject = time.strftime('Search results, %b %d, %Y')
    content = StringIO()
    writeln = partial(writeline, content)
    if search_result:
        writeln("Search results for request \"%s\" at %s" %
                (original_query, time.strftime("%H:%M:%S on %B %d, %Y"))
                )
        for i, item in enumerate(search_result):
            writeln("#1: \"%s\" by %s" % (item.book_title, item.author))
            writeln("Chapters: " + item.chapters)
    else:
        writeln("Unfortunately, nothing found "
                "for your request \"%s\" at %s" %
                (original_query, time.strftime("%H:%M:%S on %B %d, %Y"))
                )
    value = content.getvalue()
    content.close()
    return subject, value


@celery_app.task
def process_query_and_email(query, email, time):
    from django.core.mail import send_mail
    query_parts = decompose_query(query)
    books_qs = fetch_books(query_parts)
    search_result = digest_searchresult(books_qs)
    subject, content = make_email(search_result, time, query)
    return send_mail(subject,
                     content,
                     'search-results@inbook-search-pro.com',
                     [email],
                     fail_silently=False)
