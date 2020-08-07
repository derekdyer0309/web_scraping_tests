import scrapy


class GlassesShopSpider(scrapy.Spider):
    name = 'glasses_shop'
    allowed_domains = ['www.glassesshop.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.glassesshop.com/bestsellers', callback=self.parse, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        })

    def parse(self, response):

        for product in response.xpath("//div[@id='product-lists']/div"):
            yield {
                'product_url': product.xpath(".//div[@class='product-img-outer']//a/@href").get(),
                'product_image_link': product.xpath(".//div[@class='product-img-outer']//a//img/@src").get(),
                'product_name': product.xpath(".//a[contains(@class,'product-title')]/@title").get(),
                'product_price': product.xpath(".//div[@class='p-price']//span/text()").get()
            }

        next_page = response.xpath("//a[contains(text(), 'Next Page')]/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            })


