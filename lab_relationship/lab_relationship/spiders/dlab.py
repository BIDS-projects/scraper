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
import os

# DYNAMIC ITEM REFERNCE: (http://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped)
# Network Analysis Algorithms: https://networkx.github.io/documentation/latest/reference/algorithms.html

# TODOS IN THE ORDER OF PRIORITY
# TODO: limit the nubmer of webpages visited
## http://stackoverflow.com/questions/34452788/scrapy-linkextractor-limit-the-number-of-pages-crawled-per-url
# TODO: introduce depth limit
# TODO: store in the correct database
## MONGO DB integration: https://realpython.com/blog/python/web-scraping-and-crawling-with-scrapy-and-mongodb/
# TODO: improve text collection (clean)
# TODO: fix the qb3 bug (if the seed url contains path, it fails)
# TODO: exit if you are on one path for too long (amplab, jenkins) OR Naive Bayes

class MappingItem(dict, BaseItem):
    pass

class DlabSpider(scrapy.Spider):
    name = "dlab"
    output_filename = "result.json"
    page_limit = 3

    def __init__(self):
        item = MappingItem()
        self.loader = ItemLoader(item)
        self.filter_urls = list()
        self.requested_page_counter = dict()

    def start_requests(self):
        prefix = os.path.dirname(os.path.realpath(__file__))
        #filename = "data-science-websites.csv"
        filename = "debug.csv"
        try:
            with open(os.path.join(prefix, filename), 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                for row in reader:
                    seed_url = row[1].strip()
                    base_url = urlparse(seed_url).netloc
                    self.filter_urls.append(base_url)
                    # Starts from 1 since the seed page will be always crawled
                    self.requested_page_counter[base_url] = 1
                    request = Request(seed_url, callback=self.parse_seed)
                    request.meta['base_url'] = base_url
                    self.logger.info("'{}' REQUESTED".format(seed_url))
                    yield request
        except IOError:
            raise CloseSpider("A list of websites are needed")

    def parse_seed(self, response):
        self.logger.info("PARSED LINK: {}".format(response.url))
        base_url = response.meta['base_url']
        # handle external redirect while still allowing internal redirect
        if urlparse(response.url).netloc != base_url:
            return

        # adding outbound hyperlinks
        external_le = LinkExtractor(deny_domains=base_url)
        external_links = external_le.extract_links(response)
        """
        for external_link in external_links:
            # filter_urls filters out external links that are not on the list
            if urlparse(external_link.url).netloc in self.filter_urls:
                self.loader.add_value(base_url, external_link.url)
        """

        # TODO: Texts need to be cleaned (remove things like u'\n    ', u'\n        \n  \n  \n      ')
        text = response.xpath("//text()").extract()
        # TODO: Add to the correct database (make sure to add under one base_url)

        internal_le = LinkExtractor(allow_domains=base_url)
        internal_links = internal_le.extract_links(response)

        for internal_link in internal_links:
            if self.requested_page_counter[base_url] >= self.page_limit:
                break
            self.requested_page_counter[base_url] += 1
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            request.meta['dont_redirect'] = True
            self.logger.info("REQUESTED LINK: {}".format(internal_link.url))
            yield request

    def get_external_links(self, base_url, response):
        pass

    def get_internal_links(self, base_url, response):
        pass

    def closed(self, reason):
        # remove
        self.loader.add_value(None, self.requested_page_counter)
        output = self.loader.load_item()
        self.logger.info("@@@@: {}".format(output))
        with open(self.output_filename, 'w') as outfile:
            json.dump(output, outfile, sort_keys=True, indent=4, separators=(',', ': '))
