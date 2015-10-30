# -*- coding: utf-8 -*-
from urlparse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
import scrapy
import csv
import json


# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> perform analysis

# REFERNCE: (http://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped)


class MappingItem(dict, BaseItem):
    pass

class DlabSpider(scrapy.Spider):
    name = "dlab"
    output_filename = "result.json"

    def __init__(self):
        item = MappingItem()
        self.loader = ItemLoader(item)

    def start_requests(self):
        filename = "data-science-websites.csv"
        try:
            with open(filename, 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                #### DEBUG ####
                #requests = []
                #row = next(reader)
                #seed_url = row[1].strip()
                #base_url = urlparse(seed_url).netloc
                #request = Request(seed_url, callback=self.parse_seed)
                #request.meta['base_url'] = base_url
                #requests.append(request)
#
                #row = next(reader)
                #seed_url = row[1].strip()
                #base_url = urlparse(seed_url).netloc
                #request = Request(seed_url, callback=self.parse_seed)
                #request.meta['base_url'] = base_url
                #requests.append(request)
                #return requests # FOR DEBUGGING PURPOSE
                #### DEBUG ####

                for row in reader:
                    seed_url = row[1].strip()
                    base_url = urlparse(seed_url).netloc
                    request = Request(seed_url, callback=self.parse_seed)
                    request.meta['base_url'] = base_url
                    yield request
        except IOError:
            raise CloseSpider("A list of websites are needed")

    def parse_seed(self, response):
        base_url = response.meta['base_url']
        # handle external redirect while still allowing internal redirect
        if urlparse(response.url).netloc != base_url:
            return
        external_le = LinkExtractor(deny_domains=base_url)
        external_links = external_le.extract_links(response)
        for external_link in external_links:
            #TODO: if the url on the list
            self.loader.add_value(base_url, external_link.url)

        internal_le = LinkExtractor(allow_domains=base_url)
        internal_links = internal_le.extract_links(response)

        for internal_link in internal_links:
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            yield request

    def get_external_links(self, base_url, response):
        pass

    def get_internal_links(self, base_url, response):
        pass

    def closed(self, reason):
        output = self.loader.load_item()
        self.logger.info("@@@@: {}".format(output))
        with open(self.output_filename, 'w') as outfile:
            json.dump(output, outfile, sort_keys=True, indent=4, separators=(',', ': '))

