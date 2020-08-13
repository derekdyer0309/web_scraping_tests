import scrapy
from scrapy_splash import SplashRequest


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js/', callback=self.parse, endpoint='execute', args={
            'lua_source': self.script
        })

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'author': quote.xpath(".//span[2]/small/text()").get(),
                'quote': quote.xpath(".//span[@class='text']/text()").get(),
                'tags': quote.xpath(".//div[@class='tags']/a[@class='tag']/text()").getall()
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            abs_url = f"http://quotes.toscrape.com{next_page}"
            yield SplashRequest(url=abs_url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script
            })
