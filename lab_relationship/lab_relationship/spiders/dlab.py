# -*- coding: utf-8 -*-
from lab_relationship.items import Links
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import csv


# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> perform analysis
# TODO: aggregate external links under one key (base url)
# TODO: generalize to multiple websites
# TODO: only collect external links on the list
# TODO: set delay time

class DlabSpider(CrawlSpider):
    name = "dlab"
    allowed_domains = ["dlab.berkeley.edu"]
    start_urls = ["http://www.dlab.berkeley.edu"]
    rules = [
        Rule(LinkExtractor(allow_domains="dlab.berkeley.edu"), callback='parse_link'),
    ]

    """
    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                for row in reader:
                    self.start_urls += row[1]
                    print(self.start_urls)
        return
    """
                
    def parse_link(self, response):
        """ finds all external links"""
        external_le = LinkExtractor(deny_domains="dlab.berkeley.edu")
        external_links = external_le.extract_links(response)
        item = Links()
        item['url'] = response.url
        item['external'] = []
        for link in external_links:
            item['external'].append(link.url)

        yield item
