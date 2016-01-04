# -*- coding: utf-8 -*-
# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> perform analysis
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

# DYNAMIC ITEM REFERNCE: (http://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped)
# Network Analysis Algorithms: https://networkx.github.io/documentation/latest/reference/algorithms.html

# TODO: fix the qb3 bug (if the seed url contains path, it fails)
# TODO: exit if you are on one path for too long (amplab, jenkins)

class MappingItem(dict, BaseItem):
    pass

import os

class DlabSpider(scrapy.Spider):
    name = "dlab"
    output_filename = "result.json"

    def __init__(self):
        item = MappingItem()
        self.loader = ItemLoader(item)
        self.filter_urls = list()

    def start_requests(self):
        prefix = os.path.dirname(os.path.realpath(__file__))
        filename = "data-science-websites.csv"
        try:
            with open(os.path.join(prefix, filename), 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                for row in reader:
                    seed_url = row[1].strip()
                    base_url = urlparse(seed_url).netloc
                    self.filter_urls.append(base_url)
                    request = Request(seed_url, callback=self.parse_seed)
                    request.meta['base_url'] = base_url
                    self.logger.info("'{}' REQUESTED".format(seed_url))
                    yield request
        except IOError:
            raise CloseSpider("A list of websites are needed")

    def parse_seed(self, response):
        self.logger.info("IN PARSE_SEED FOR {}".format(response.url))
        base_url = response.meta['base_url']
        # handle external redirect while still allowing internal redirect
        if urlparse(response.url).netloc != base_url:
            return
        external_le = LinkExtractor(deny_domains=base_url)
        external_links = external_le.extract_links(response)
        for external_link in external_links:
            if urlparse(external_link.url).netloc in self.filter_urls:
                self.loader.add_value(base_url, external_link.url)

        internal_le = LinkExtractor(allow_domains=base_url)
        internal_links = internal_le.extract_links(response)

        for internal_link in internal_links:
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            request.meta['dont_redirect'] = True
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
