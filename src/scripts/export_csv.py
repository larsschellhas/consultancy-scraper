import json
import csv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    """ This is the main method for exporting consultancy contacts """

    items = []
    fieldnames = ['company_name', "company_street", 'company_PLZ', 'company_city', 'company_country', 'company_phone', 'company_website', 'company_email', 'company_sectors', 'consulting_de_url', 'company_type']
    
    with open("src/consultancy_scraper/consultancies.json") as file:
        items = json.load(file)

    with open("src/consultancy_scraper/consultancies.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)


if __name__ == "__main__":
    main()
