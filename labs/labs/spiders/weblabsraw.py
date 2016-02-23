# -*- coding: utf-8 -*-

from urlparse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as LE
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.conf import settings
from labs.items import HTMLItem
import scrapy
import csv
import json
import os


class WebLabsRawSpider(scrapy.Spider):
    """Crawls given CSV and yields raw HTML"""

    name = "weblabsraw"

    def __init__(self, *args):
        self.domains = set()
        self.counts = {}
        self.seed_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'data-science-websites.csv')

    def request(self, url, **meta):
        """create request object"""
        return Request(url, callback=self.parse, meta=meta)

    @staticmethod
    def domain(url):
        """returns domain from url"""
        return urlparse(url).netloc

    def start_requests(self):
        """Begin requests for using initial csv"""
        with open(self.seed_path, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            for _, url in reader:
                url = url.strip()
                domain = self.domain(url)
                self.domains.add(domain)
                self.counts.setdefault(domain, 0)
                self.counts[domain] += 1
                yield self.request(url)

    def parse(self, response):
        """Parse response and yield new requests"""
        domain = self.domain(response.url)
        self.counts[domain] += 1

        if domain in self.domains and \
            self.counts[domain] < settings['WEBSITE_PAGES_LIMIT']:

            html, links = self.extract_data(response)

            self.html = html # hack
            yield html
            for link in links:
                yield self.request(link.url)

    def extract_data(self, response, update={}):
        """Get all important data from a response object and return"""
        data = vars(response).copy()
        links = LE(allow_domains=self.domains).extract_links(response)

        return HTMLItem(
            url=str(data['_url']),
            body=str(data['_body']),
            request=str(data['request']),
            links=links), links
