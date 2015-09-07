import re, io
from datetime import datetime

from django.core.mail import send_mail
from django.db.models import Q, Prefetch

from . import celery_app
from book_store.models import Book, Page
from collections import namedtuple

SearchResultItem = namedtuple('SearchResultItem',
                              ('book_title', 'chapters', 'author'))


def decompose_query(query):
    words = re.split('\W+', query)
    seen = set()
    return [x.lower() for x in words
            if x.lower() not in seen and
            not seen.add(x.lower())
            ]

def fetch_books(query_parts):
    query_cond = Q()
    for word in query_parts:
        query_cond |= Q(text__search=word)
    books = Book.objects \
        .select_related('author') \
        .prefetch_related(
            Prefetch('chapter__page',
                     queryset=Page.objects.filter(query_cond))
        ).all()
    return books


def digest_searchresult(books):
    result = []
    for book in books:
        item = SearchResultItem(
            book_title=book.title,
            chapters=', '.join(
                '%d (pages %s)' % (ch.chapter_nubmer,
                                   ', '.join(str(p.page_number)
                                             for p in ch.pages)
                                   )
                for ch in book.chapters
            ),
            author=book.author
        )
        result.append(item)
    return result


def make_email(search_result, time, original_query):
    subject = time.strftime('Search results, %b %d, %Y')
    content = io.StringIO()
    if search_result:
        content.write("Search results for request \"%s\" at %s" %
                      (original_query, time.strftime("%H:%M:%S on %B %d, %Y"))
                      )
        for i, item in enumerate(search_result):
            content.write("#1: \"%s\" by %s" % (item.book_title, item.author))
            content.write("Chapters: " + item.chapters)
    else:
        content.write("Unfortunately, nothing found "
                      "for your request \"%s\" at %s" %
                      (original_query, time.strftime("%H:%M:%S on %B %d, %Y"))
                      )
    value = content.getvalue()
    content.close()
    return subject, value


@celery_app.task
def process_query_and_email(query, email, time):
    # to demonstrate that search can last
    # for big amount of time, we make a 5-second delay
    from time import sleep
    sleep(5)
    query_parts = decompose_query(query)
    books_qs = fetch_books(query_parts)
    search_result = digest_searchresult(books_qs)
    subject, content = make_email(search_result, time, query)
    return send_mail(subject,
                     content,
                     'search-results@inbook-search-pro.com',
                     [email],
                     fail_silently=False)
