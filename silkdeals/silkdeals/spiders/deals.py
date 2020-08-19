import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class DealsSpider(scrapy.Spider):
    name = 'deals'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://duckduckgo.com",
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )
        
    def parse(self, response):
        # with open('image.png', 'wb') as image_file:
        #     image_file.write(response.meta['screenshot'])
        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath('//input[@id="search_form_input_homepage"]')
        search_input.send_keys('Hello World')
        
        search_input.send_keys(Keys.ENTER)

        html = driver.page_source
        response_obj = Selector(text=html)
        
        links = response_obj.xpath("//div[@class='result__extras__url']/a")
        for link in links:
            yield{
                'url': link.xpath(".//@href").get()
            }
