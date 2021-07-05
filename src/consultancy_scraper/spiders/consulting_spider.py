import scrapy
import re
import urllib.parse
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from consultancy_scraper.items import Consultancy


class ConsultingSpiderSpider(CrawlSpider):
    name = 'consulting_spider'
    allowed_domains = ['consulting.de']
    start_urls = ['https://www.consulting.de/anbieter-leistungen/unternehmensberatung/unternehmensliste/energiewirtschaft-energieversorgung/']

    rules = (
        Rule(LinkExtractor(allow=r'anbieter-leistungen/unternehmensberatung/unternehmensliste/energiewirtschaft-energieversorgung/'), follow=True),
        Rule(LinkExtractor(allow=r'anbieter-leistungen/unternehmensberatung/consultingunternehmen/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = Consultancy()
        item['consulting_de_url'] = response.url
        item['company_name'] = urllib.parse.unquote(re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[3]/div/div[1]/div/div/div[1]/p/text()[1]').get()))
        item['company_street'] = urllib.parse.unquote(re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[3]/div/div[1]/div/div/div[1]/p/text()[3]').get()))
        plz_city = response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[3]/div/div[1]/div/div/div[1]/p/text()[4]').get()
        plz_city = re.sub('^[\s\xA0]+|[\s\xA0]+$', '', urllib.parse.unquote(plz_city)).split(' ')
        item['company_PLZ'] = plz_city.pop(0)
        item['company_city'] = ' '.join(plz_city)
        item['company_country'] = urllib.parse.unquote(re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[3]/div/div[1]/div/div/div[1]/p/text()[5]').get()))
        item['company_phone'] = urllib.parse.unquote(re.sub('[\(\) a-zA-Z\.\:-]','', re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[3]/div/div[1]/div/div/div[2]/p/text()[1]').get()).replace('(0)','')))
        soup = BeautifulSoup(urllib.parse.unquote(re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[3]/div/div[1]/div/div/div[2]/p/a[1]').get())))
        item['company_email'] = soup.a.text
        soup = BeautifulSoup(urllib.parse.unquote(re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[3]/div/div[1]/div/div/div[2]/p/a[2]').get())))
        item['company_website'] = soup.a.get('href')
        item['company_type'] = urllib.parse.unquote(re.sub('^[\s\xA0]+|[\s\xA0]+$', '', response.xpath('/html/body/div/div[2]/div[5]/div[1]/div[1]/div/article/div[1]/div/p/text()').get()).replace('\r\n\t\t\t\t\t-', '')).split(', ')
        return item
