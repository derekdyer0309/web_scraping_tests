import scrapy
from scrapy.exceptions import CloseSpider
import json


class BooksSpider(scrapy.Spider):
    name = 'books'

    INCREMENTED_BY=12
    offset=0
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12']

    def parse(self, response):
        if response.status==500:
            raise CloseSpider('Reached last page...')

        resp = json.loads(response.body)
        books = resp.get('works')

        for book in books:
            yield {
                'title': book.get('title'),
                'subject': book.get('subject'),
                'author(s)': book.get('authors')
            }

        self.offset+=self.INCREMENTED_BY
        
        yield scrapy.Request (
            url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',
            callback=self.parse
        )
