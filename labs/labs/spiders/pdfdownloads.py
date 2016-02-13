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
import re

class PDFSpider(scrapy.Spider):
    name = "pdf"
    page_limit = 5

    def __init__(self):
        '''
        Set up the researcher database.
        '''
        self.researcherDatabase = {}
        self.visited = set()
        self.toVisit = set()
        with open("filtered.db") as f:
            for line in f:
                lineSplit = line.split("@")
                name = lineSplit[0].split(" ")
                self.researcherDatabase[name[0][0] + " " + name[-1]] = (lineSplit[0], lineSplit[2].split("~"))

    def start_requests(self):
        '''
        Starts the spider with a specified researcher.
        '''
        self.researcher = 'Pieter Abbeel'
        self.researcherKey = self.researcher[0] + " " + self.researcher.split(" ")[-1]
        self.index = -20
        self.ranOutOfLinks = False
        self.pageCounter = 0
        self.visited.add(self.researcher)
        yield Request(self.next_URL(), callback = self.parse_seed)

    def next_URL(self):
        '''
        Updates and returns the next URL to scrape.
        '''
        if self.ranOutOfLinks:
            self.researcher = self.toVisit.pop()
            self.visited.add(self.researcher)
            self.researcherKey = self.researcher[0] + " " + self.researcher.split(" ")[-1]
            self.index = 0
            self.ranOutOfLinks = False
        else:
            self.index += 20
        self.pageCounter += 1
        if self.pageCounter >= PDFSpider.page_limit:
            raise CloseSpider("Page limit exceeded.")
        return ("https://scholar.google.com/scholar?start=" + str(self.index)
            + '&q=filetype:pdf+author:"' + self.researcher
            + '"&hl=en&num=20&as_sdt=1,5&as_vis=1')

    def parse_seed(self, response):
        '''
        Parses the website, adds researchers, and yields the items.
        '''

        # for link in response.xpath('//a[contains(@href, "oi=sra")]/text()'):
        #     name = link.extract()
        #     name = name[0] + " " + name.split(" ")[-1]
        #     if name in self.researcherDatabase:
        #         fullName = self.researcherDatabase[name][0]
        #         if fullName not in self.visited:
        #             print "ADDING %s TO THE VISITNG LIST" % fullName
        #             self.toVisit.add(fullName)

        for link in response.xpath("//div[@class='gs_a']"):
            lines = link.extract()[18:].split(" - ")
            names = lines[0].split(",")
            for name in names:
                name = name.strip()
                if "href" in name:
                    name = re.split('>', name)
                    name = name[1][:-3]
                name = name[0] + " " + name.split(" ")[-1]
                if name in self.researcherDatabase:
                    fullName = self.researcherDatabase[name][0]
                    if fullName not in self.visited:
                        print "ADDING %s TO THE VISITNG LIST" % fullName
                        self.toVisit.add(fullName)

        links = response.xpath('//a[contains(@href, ".pdf")]')
        if not links:
            self.ranOutOfLinks = True
        secondLink = False
        for link in links:
            if secondLink:
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
                    paper_item['department'] = ",".join(self.researcherDatabase[self.researcherKey][1])
                    secondLink = False
                    print "RETRIEVED PAPER " + pdfURL
                    print "CURRENT RESEARCHER " + self.researcher
                    yield paper_item
            else:
                secondLink = True

        yield Request(self.next_URL(), callback = self.parse_seed)
