# -*- coding: utf-8 -*-
from urlparse import urlparse
from lab_relationship.items import Links
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import scrapy
import csv
import json


# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> perform analysis
# TODO: generalize to multiple websites

# REFERNCE: (http://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped)

from scrapy.item import BaseItem
from scrapy.contrib.loader import ItemLoader
from scrapy.exceptions import CloseSpider

class FlexibleItem(dict, BaseItem):
    pass

class DlabSpider(scrapy.Spider):
    name = "dlab"
    def __init__(self):
        #self.mapping = dict()
        item = FlexibleItem()
        self.loader = ItemLoader(item)

    def start_requests(self):
        filename = "data-science-websites.csv"
        try:
            with open(filename, 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                # don-han.com
                row = next(reader)
                seed_url = row[1].strip()
                base_url = urlparse(seed_url).netloc
                #self.mapping[base_url] = set()
                #item = Links(base_url=seed_url, on_list=[], off_list=[])
                request = Request(seed_url, callback=self.parse_seed)
                request.meta['base_url'] = base_url
                #requests.append(request)
                yield request
                # amplab
            # yield request
                #for row in reader:
                    #seed_url = row[1]
                    #item = Links(url=seed_url, on_list=[], off_list=[])
                    #request = Request(seed_url, callback=self.parse_seed)
                    #request.meta['item'] = item
                    #yield request
        except IOError:
            raise CloseSpider("A list of websites are needed")

    def parse_seed(self, response):
        base_url = response.meta['base_url']
        external_le = LinkExtractor(deny_domains=base_url)
        external_links = external_le.extract_links(response)
        for external_link in external_links:
            # if the url on the list
#            self.mapping[base_url].add(external_link.url)
            self.loader.add_value(base_url, external_link.url)

        internal_le = LinkExtractor(allow_domains=base_url)
        internal_links = internal_le.extract_links(response)

        for internal_link in internal_links:
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            yield request

    def closed(self, reason):
        self.logger.info("@@@@: {}".format(self.loader.load_item()))
        return self.loader.load_item()
