# -*- coding: utf-8 -*-
import scrapy


class GetInstitutionsSpider(scrapy.Spider):
    name = "get_institutions"
    allowed_domains = ["vcresearch.berkeley.edu"]
    start_urls = (
        'http://vcresearch.berkeley.edu/datascience/domain-science-programs',
        'http://vcresearch.berkeley.edu/datascience/methods-programs'
    )

    def parse(self, response):
        pass
