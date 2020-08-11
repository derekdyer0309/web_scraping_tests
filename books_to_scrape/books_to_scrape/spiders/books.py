import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//article[@class='product_pod']/h3/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), follow=True, process_request='set_user_agent'),
    )

    def start_requests(self):
        yield scrapy.Request(url="http://books.toscrape.com/index.html", headers={
            'user-agent': self.user_agent
        })

    def set_user_agent(self, request, spider):
        request.headers['user-agent'] = self.user_agent,
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//h1/text()").get(),
            'price': response.xpath("//p[@class='price_color']/text()").get(),
            'description': response.xpath("(//p)[4]/text()").get(),
            'upc': response.xpath("(//td)[1]/text()").get(),
            'book_url': response.url,
            'user-agent': response.request.headers["user-agent"].decode('utf-8')
        }
