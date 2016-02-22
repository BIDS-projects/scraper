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
import scrapy
import csv
import json


class MappingItem(dict, BaseItem):
    pass


class WebLabsRawSpider(scrapy.Spider):
    name = "weblabsraw"

    def __init__(self, *args):
        self.loader = ItemLoader(MappingItem())
        self.filter_urls = []

    def start_requests(self):
        """Begin requests for DLab"""
        reader = map(lambda x: x.split(','), seed.strip().split('\n'))
        for _, seed_url in reader:
            seed_url = seed_url.strip()
            base_url = urlparse(seed_url).netloc
            self.filter_urls.append(base_url)
            request = Request(seed_url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            yield request

    def parse_seed(self, response):
        """Parse response and yield both HTML and new requests"""

        base_url = response.meta['base_url']

        # allow internal redirects
        if urlparse(response.url).netloc == base_url:
            yield self.parse_response(response)

            # add external links to loader?
            for link in self.parse_external_links(base_url, response):
                self.loader.add_value(base_url, link.url)

            # yield requests only for internal links
            for link in self.parse_internal_links(base_url, response):
                request = Request(link.url, callback=self.parse_seed)
                request.meta.update({'base_url':base_url, 'dont_redirect':True})
                yield request

    def parse_response(self, response):
        """Get all data from a response object and return"""
        data = vars(response).copy()

        raise UserWarning(data['request'].keys())
        data.update({
            '_body':str(data['_body']),
            'request':vars(data['request'])
        })
        return data

    def parse_external_links(self, base_url, response):
        """Return external links using response"""
        return filter(lambda link:urlparse(link.url).netloc in self.filter_urls,
            LinkExtractor(deny_domains=base_url).extract_links(response))

    def parse_internal_links(self, base_url, response):
        """Return internal links using response"""
        return LinkExtractor(allow_domains=base_url).extract_links(response)
