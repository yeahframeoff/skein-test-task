import re

from more_itertools import chunked

from book_store.models import Book, Author, Page, Chapter

tolkien = Author.objects.create(name='John',
                                last_name='Ronald Ruel Tolkien',
                                bio='')

hobbit_book = Book.objects.create(title='The Hobbit',
                                  author=tolkien)

with open('hobbit.txt') as f:
    text = f.readlines()
text = '\n'.join(text)
text = re.sub('\n+', '\n', text)
chapters = re.split(r'Chapter \w+\n', text)
chapters = (ch.strip() for ch in chapters if ch.strip())

page_no = 0
for i, chapter in enumerate(chapters, 1):
    lines = chapter.split('\n')
    title = lines.pop(0)
    ch = Chapter.objects.create(title=title,
                                chapter_number=i,
                                book=hobbit_book)
    pages = chunked(lines, 4)
    page_objs = []
    for page_text in pages:
        page_no += 1
        page_obj = Page(page_number=page_no,
                        text='\n'.join(page_text),
                        chapter=ch)
        page_objs.append(page_obj)
    Page.objects.bulk_create(page_objs)
