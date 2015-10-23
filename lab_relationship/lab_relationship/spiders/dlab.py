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
                #item = Links(base_url=seed_url, on_list=[], off_list=[])
                self.mapping[seed_url] = []
                request = Request(seed_url, callback=self.parse_seed)
                request.meta['item'] = item
                requests.append(request)
            return requests
                # amplab
            if False:
                row = next(reader)
                seed_url = row[1].strip()
                item = Links(base_url=seed_url, on_list=[], off_list=[])
                request = Request(seed_url, callback=self.parse_seed)
                request.meta['item'] = item
                requests.append(request)
            return requests
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
        item = response.meta['item']
        netloc = urlparse(item['base_url']).netloc
        external_le = LinkExtractor(deny_domains=netloc)
        external_links = external_le.extract_links(response)
        for external_link in external_links:
            # if the url on the list
            item['on_list'].append(external_link)

        internal_le = LinkExtractor(allow_domains=netloc)
        internal_links = internal_le.extract_links(response)

        for internal_link in internal_links:
            self.logger.info("@@@@@@@@: {}".format(internal_link.url))
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['item'] = item
            yield request

    """
    def parse_url(self, response):
        external_le = LinkExtractor(deny_domains="dlab.berkeley.edu")
        external_links = external_le.extract_links(response)
        item = Links()
        item['url'] = response.url
        item['on_list'] = []
        for link in external_links:
            item['on_list'].append(link.url)
        yield item
    """
