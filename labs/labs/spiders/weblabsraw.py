# -*- coding: utf-8 -*-
# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> save as HTML
from urlparse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.selector import HtmlXPathSelector
from labs.items import LinkItem, HTMLItem
import scrapy
import csv
import json
import os


class WebLabsRawSpider(scrapy.Spider):
    """Crawls given CSV and yields raw HTML"""

    name = "weblabsraw"

    def __init__(self, *args):
        self.loader = ItemLoader(BaseItem())
        self.urls = set()
        self.seed_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data-science-websites.csv')
        self.request = lambda url: Request(url, callback=self.parse_response)

    def start_requests(self):
        """Begin requests for using initial csv"""
        with open(self.seed_path, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            for _, seed_url in reader:
                self.urls.add(urlparse(seed_url).netloc)
                yield self.request(seed_url.strip())

    def parse_response(self, response):
        """Parse response and yield both HTML and new requests"""
        if urlparse(response.url).netloc not in self.urls:
            return

        html, links = self.extract_data(response)

        yield html
        for link in links:
            self.loader.add_value(link.url)
            yield self.request(link.url)

    def extract_data(self, response, update={}):
        """Get all important data from a response object and return"""
        data = vars(response).copy()
        links = LinkExtractor(allow_domains=self.urls).extract_links(response)

        return HTMLItem(
            url=str(data['_url']),
            body=str(data['_url']),
            request=str(data['_url']),
            links=links), links
