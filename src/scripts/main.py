import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

items = []

class ItemListGeneratorPipeline():
    """ A pipeline to add all items to the main list """

    def __init__(self):
        self.ids_seen = set()

    def process_items(self, item, spider):
        items.append(item)


def main():
    """ This is the main method for sending emails to consultancies """
    
    settings = get_project_settings()
    settings['ITEM_PIPELINES']['__main__.ItemListGeneratorPipeline'] = 100
    process = CrawlerProcess(settings)

    process.crawl('consulting_spider', domain='consulting.de')
    process.start() # the script will block here until the crawling is finished
    
    pass


if __name__ == "__main__":
    main()