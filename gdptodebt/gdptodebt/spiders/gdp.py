import scrapy
import logging


class GdpSpider(scrapy.Spider):
    name = 'gdp'
    allowed_domains = ['www.worldpopulationreview.com']
    start_urls = ['http://www.worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//tbody//tr")
        for country in countries:
            name = country.xpath(".//a//text()").get()
            gdp = country.xpath(".//td[2]/text()").get()
            population = country.xpath(".//td[3]/text()").get()
            

            yield {
                'name': name,
                'gdp': gdp,
                'population': population
            }
