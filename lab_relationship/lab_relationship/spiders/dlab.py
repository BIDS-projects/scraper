# -*- coding: utf-8 -*-
# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> perform analysis
from urlparse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from lab_relationship.items import LinkItem, TextItem
import scrapy
import csv
import json
import os
import datetime

# DYNAMIC ITEM REFERNCE: (http://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped)
# Network Analysis Algorithms: https://networkx.github.io/documentation/latest/reference/algorithms.html
# TODOS IN THE ORDER OF PRIORITY

# TODO: fix the qb3 bug (if the seed url contains path, it fails)
# TODO: exit if you are on one path for too long (amplab, jenkins) OR Naive Bayes

# Potential Things To Do
# TODO: introduce depth limit 

# Store different item into different collections in MongoDB
# processing different item in one pipeline: https://github.com/scrapy/scrapy/issues/102
class DlabSpider(scrapy.Spider):
    name = "dlab"
    page_limit = 5

    def __init__(self):

        self.filter_urls = list()
        self.requested_page_counter = dict()

    def start_requests(self):
        prefix = os.path.dirname(os.path.realpath(__file__))
        #filename = "data-science-websites.csv"
        filename = "1debug.csv"
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
        external_links = self.get_external_links(base_url, response)

        for external_link in external_links:
            # filter_urls filters out external links that are not on the list
            if urlparse(external_link.url).netloc in self.filter_urls:
                link_item = LinkItem()
                link_item['base_url'] = base_url
                link_item['url'] = response.url
                link_item['link'] = external_link.url
                link_item['timestamp'] = datetime.datetime.now()
                yield link_item

        text =  filter(None, [st.strip() for st in response.xpath("//*[not(self::script or self::style)]/text()[normalize-space()]").extract()])
        text = ' '.join(text)

        text_item = TextItem()
        text_item['base_url'] = base_url
        text_item['url'] = response.url
        text_item['text'] = text
        text_item['timestamp'] = datetime.datetime.now()
        yield text_item


        for internal_link in self.get_internal_links(base_url, response):
            if self.requested_page_counter[base_url] >= self.page_limit:
                break
            self.requested_page_counter[base_url] += 1
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            request.meta['dont_redirect'] = True
            self.logger.info("REQUESTED LINK: {}".format(internal_link.url))
            yield request

    def get_external_links(self, base_url, response):
        return LinkExtractor(deny_domains=base_url).extract_links(response)

    def get_internal_links(self, base_url, response):
        return LinkExtractor(allow_domains=base_url).extract_links(response)
