import scrapy
import re
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from consultancy_scraper.items import Consultancy


class WlwSpiderSpider(CrawlSpider):
    name = 'wlw_spider'
    allowed_domains = ['wlw.de']
    start_urls = [
        'https://www.wlw.de/de/suche?locationName=Deutschland&q=Ingenieurb%C3%BCro%20energietechnik']

    rules = (
        Rule(LinkExtractor(
            allow=r'\?locationName=Deutschland&q=Ingenieurb%C3%BCro%20energietechnik'), follow=True),
        Rule(LinkExtractor(allow=r'de/firma/'),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        countries = {
            "DE": "Deutschland",
        }
        item = Consultancy()
        item['original_url'] = response.url
        item['company_name'] = re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath(
            '//*[@id="contact-location"]/div/div[1]/div[2]/div/address/strong/text()').get())
        item['company_street'] = re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath(
            '//*[@id="contact-location"]/div/div[1]/div[2]/div/address/div/div[1]/text()').get())
        plz_city = response.xpath(
            '//*[@id="contact-location"]/div/div[1]/div[2]/div/address/div/div[2]/text()').get()
        plz_city = re.sub('^[\s\xA0]+|[\s\xA0]+$', '', plz_city).split(' ')
        country_plz = plz_city.pop(0).split('-')
        if len(country_plz) > 1:
            item['company_country'] = countries[country_plz.pop(0)]
        else:
            item['company_country'] = countries["DE"]
        item['company_PLZ'] = country_plz.pop(0)
        item['company_city'] = ' '.join(plz_city)
        item['company_phone'] = re.sub('[\(\) a-zA-Z\.\:-]', '', re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath(
            '//*[@id="location-and-contact__phone"]/span/span/div/a/span/text()').get()).replace('(0)', ''))
        item['company_email'] = re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath(
            '//*[@id="location-and-contact__email"]/span/text()').get())
        website_soup = BeautifulSoup(response.xpath('//*[@id="location-and-contact__website"]').get())
        item['company_website'] = website_soup.a.get('href')
        item['company_type'] = []
        item['company_sectors'] = []
        return item
