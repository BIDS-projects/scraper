# -*- coding: utf-8 -*-
# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> perform analysis
from urlparse import urlparse
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from labs.items import *
import scrapy
import csv
import json
import os
import datetime

# DYNAMIC ITEM REFERNCE: (http://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped)
# Network Analysis Algorithms: https://networkx.github.io/documentation/latest/reference/algorithms.html

# Store different item into different collections in MongoDB
# processing different item in one pipeline: https://github.com/scrapy/scrapy/issues/102
class WebLabsSpider(scrapy.Spider):
    name = "weblabs"
    page_limit = 500

    def __init__(self):
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
                    request.meta['tier'] = -1
                    #self.logger.info("'{}' REQUESTED".format(seed_url))
                    yield request
        except IOError:
            raise CloseSpider("A list of websites are needed")

    def parse_seed(self, response):
        #self.logger.info("PARSED LINK: {}".format(response.url))
        base_url = response.meta['base_url']
        tier = response.meta['tier'] + 1

        # handle external redirect while still allowing internal redirect
        if urlparse(response.url).netloc != base_url:
            return

        # adding outbound hyperlinks
        external_links = self.get_external_links(base_url, response)

        for external_link in external_links:
            # filter_urls filters out external links that are not on the list
            """
            external_link_item = ExternalLinkItem()
            external_link_item['base_url'] = base_url
            external_link_item['src_url'] = response.url
            external_link_item['timestamp'] = datetime.datetime.now()
            if urlparse(external_link.url).netloc in self.filter_urls:
                external_link_item['dst_url'] = external_link.url
            else:
                external_link_item['non_filtered_url'] = external_link.url
            yield external_link_item
            """
            pass

        # filter removes items with zero length
        text = get_text(response)
        # to divide up into words, not each html block
        #text = text.split()

        text_item = TextItem()
        text_item['base_url'] = base_url
        text_item['src_url'] = response.url
        text_item['text'] = text
        text_item['timestamp'] = datetime.datetime.now()
        text_item['tier'] = tier
        yield text_item

        for internal_link in self.get_internal_links(base_url, response):
            if self.requested_page_counter[base_url] >= self.page_limit:
                break
            self.requested_page_counter[base_url] += 1
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            request.meta['dont_redirect'] = True
            request.meta['tier'] = tier

            """
            self.logger.info("REQUESTED LINK: {}".format(internal_link.url))
            internal_link_item = InternalLinkItem()
            internal_link_item['base_url'] = base_url
            internal_link_item['src_url'] = response.url
            internal_link_item['dst_url'] = internal_link.url
            internal_link_item['timestamp'] = datetime.datetime.now()
            internal_link_item['tier'] = tier
            self.logger.debug("current url: {}; tier: {}".format(response.url, tier))
            yield internal_link_item
            """
            yield request

    def get_text(self, response):
        text =  filter(None, [st.strip() for st in response.xpath("//*[not(self::script or self::style)]/text()[normalize-space()]").extract()])

        """
        soup = BeautifulSoup(response.body_as_unicode())
        # remove script (js) and style (css)
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        ## break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        ## break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        ## drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)
        """
        text = ' '.join(text)
        return text

    def get_external_links(self, base_url, response):
        return LinkExtractor(deny_domains=base_url).extract_links(response)

    def get_internal_links(self, base_url, response):
        return LinkExtractor(allow_domains=base_url, deny="/jenkins/").extract_links(response)

    def get_jenkins(self):
        return LinkExtractor(allow="/jenkins/").extract_links(response)
