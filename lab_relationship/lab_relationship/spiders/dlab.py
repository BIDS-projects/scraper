# -*- coding: utf-8 -*-
from urlparse import urlparse
from lab_relationship.items import Links
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import scrapy
import csv
import sys


# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> perform analysis
# TODO: generalize to multiple websites
# TODO: only collect external links of websites on the given list
# TODO: aggregate external links under one key (base url)

class DlabSpider(scrapy.Spider):
    name = "dlab"
    def __init__(self):
        self.mapping = dict()

    def start_requests(self):
        filename = "data-science-websites.csv"
        requests = []
        try:
            with open(filename, 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                # don-han.com
                row = next(reader)
                seed_url = row[1].strip()
                netloc = urlparse(seed_url).netloc
                self.mapping[netloc] = set()
                #item = Links(base_url=seed_url, on_list=[], off_list=[])
                request = Request(seed_url, callback=self.parse_seed)
                request.meta['netloc'] = netloc
                #requests.append(request)
                yield request
                # amplab
            # yield request
                #for row in reader:
                    #seed_url = row[1]
                    #self.logger.info("@@@@ THE SEED URL @@@@ :{}".format(seed_url))
                    #item = Links(url=seed_url, on_list=[], off_list=[])
                    #request = Request(seed_url, callback=self.parse_seed)
                    #request.meta['item'] = item
                    #yield request
        except IOError:
            raise scrapy.exceptions.CloseSpider("A list of websites are needed")

    def parse_seed(self, response):
        self.logger.info("@@@@@ WE ARE HERE @@@@@@")
        netloc = response.meta['netloc']
        external_le = LinkExtractor(deny_domains=netloc)
        external_links = external_le.extract_links(response)
        for external_link in external_links:
            # if the url on the list
            self.mapping[netloc].add(external_link.url)
        self.logger.info("@@@@@{}@@@@@".format(self.mapping))

        internal_le = LinkExtractor(allow_domains=netloc)
        internal_links = internal_le.extract_links(response)

        for internal_link in internal_links:
            self.logger.info("@@@@@@@@: {}".format(internal_link.url))
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['netloc'] = netloc
            yield request
