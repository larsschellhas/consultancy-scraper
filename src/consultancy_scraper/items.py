# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Consultancy(scrapy.Item):
    """Scrapy Class for Consultancies"""
    consulting_de_url = scrapy.Field()
    company_name = scrapy.Field()
    company_street = scrapy.Field()
    company_PLZ = scrapy.Field()
    company_city = scrapy.Field()
    company_country = scrapy.Field()
    company_phone = scrapy.Field()
    company_email = scrapy.Field()
    company_website = scrapy.Field()
    company_type = scrapy.Field()

