# -*- coding: utf-8 -*-
from urlparse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from labs.items import PaperItem
import scrapy
import csv
import json
import os
import datetime

class PDFSpider(scrapy.Spider):
    name = "pdf"
    page_limit = 50

    def __init__(self):
    	pass

    def start_requests(self):
        for author in ['"John DeNero"', '"Satish Rao"']:
            self.researcher = author
            index = 0
            while index < PDFSpider.page_limit:
                url = "https://scholar.google.com/scholar?start=" + str(index) + "&q=filetype:pdf+author:" + author + "&hl=en&num=20&as_sdt=1,5&as_vis=1"
                print url
                request = Request(url, callback = self.parse_seed)
                yield request
                index += 20

    def parse_seed(self, response):
        links = response.xpath('//a[contains(@href, ".pdf")]')
        firstLink = True
        for link in links:
            if firstLink:
                pdfURL = link.select('@href').extract()[0]
                os.system("curl -o research.pdf \'" + pdfURL + "\'")
                os.system("pdftotext research.pdf research.txt")
                with open("research.txt") as f:
                    paper_item = PaperItem()
                    paper_item['url'] = pdfURL
                    paper_item['researcher'] = self.researcher
                    text = f.read().split()
                    text = [word for word in text if len(word) > 2]
                    paper_item['text'] = text
                    paper_item['timestamp'] = datetime.datetime.now()
                    firstLink = False
                    print "RETRIEVED PAPER " + pdfURL
                    print "CURRENT RESEARCHER " + self.researcher
                    yield paper_item
            else:
                firstLink = True
