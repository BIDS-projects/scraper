# -*- coding: utf-8 -*-
# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> save as HTML
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
from urlparse import urlparse
import csv
import json
import scrapy


class MappingItem(dict, BaseItem):
    pass


class WebLabsRawSpider(scrapy.Spider):
    name = "weblabsraw"

    def __init__(self, *args):
        self.loader = ItemLoader(MappingItem())
        self.filter_urls = []

    def start_requests(self):
        """Begin requests for DLab."""
        reader = map(lambda x: x.split(','), seed.strip().split('\n'))
        for _, seed_url in reader:
            seed_url = seed_url.strip()
            base_url = urlparse(seed_url).netloc
            self.filter_urls.append(base_url)
            request = Request(seed_url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            request.meta['deg_sep'] = 0
            yield request

    def parse_seed(self, response):
        """Parse response and yield both HTML and new requests."""

        base_url = response.meta['base_url']
        deg_sep = response.meta['deg_sep']

        # Allow internal redirects.
        if urlparse(response.url).netloc == base_url:
            yield self.parse_response(response)

            # Add external links to loader?
            for link in self.parse_external_links(base_url, response):
                self.loader.add_value(base_url, link.url)

            # Yield requests only for internal links.
            for link in self.parse_internal_links(base_url, response):
                request = Request(link.url, callback=self.parse_seed)
                request.meta.update({'base_url': base_url, 'deg_sep': deg_sep + 1,
                    'dont_redirect': True})
                yield request

    def parse_response(self, response):
        """Get all data from a response object and return."""
        data = vars(response).copy()
        data.update({
            '_body': str(data['_body']),
            'request': vars(data['request'])
        })
        return data

    def parse_external_links(self, base_url, response):
        """Return external links using response."""
        return filter(lambda link: urlparse(link.url).netloc in self.filter_urls,
            LinkExtractor(deny_domains=base_url).extract_links(response))

    def parse_internal_links(self, base_url, response):
        """Return internal links using response."""
        return LinkExtractor(allow_domains=base_url).extract_links(response)


seed = """
AMPLab, https://amplab.cs.berkeley.edu/
Archaeological Research Facility (ARF), http://arf.berkeley.edu/
Berkeley Atmospheric Sciences Center (BASC), http://www.atmos.berkeley.edu/
Berkeley Center for Cosmological Physics, http://bccp.berkeley.edu/
Berkeley Center for New Media, http://bcnm.berkeley.edu/
Berkeley Initiative in Global Change Biology (BiGCB), http://globalchange.berkeley.edu/
Berkeley KamLAND Group, http://kamland.lbl.gov/
Berkeley Nanosciences and Nanoengineering Institute (BNNI), http://nano.berkeley.edu/welcome/welcome.html
Berkeley Natural History Museums (BNHM), http://bnhm.berkeley.edu/
Berkeley Research Computing, http://research-it.berkeley.edu/programs/berkeley-research-computing
Berkeley Seismological Laboratory, http://seismo.berkeley.edu/
BIDS, http://bids.berkeley.edu
California Census Research Data Center (CCRDCs), http://www.ccrdc.ucla.edu/
California Digital Library, http://www.cdlib.org/
California Institute for Science and Innovation (QB3), http://www.qb3.org/
Center for Causal Inference, http://igs.berkeley.edu/research/center-for-causal-inference
Center for Computational Biology (CCB), http://qb3.berkeley.edu/ccb/
Center for Long-Term Cybersecurity, http://www.ischool.berkeley.edu/cltc
Center for Time Domain Informatics (CTDI), https://sites.google.com/site/cftdinfo/
CITRIS , http://citris-uc.org/
CollectionSpace, http://www.collectionspace.org/
Computational Cognitive Science Lab, http://cocosci.berkeley.edu/
Computational Cosmology Center (C³), http://crd.lbl.gov/groups-depts/computational-cosmology-center/
Computational Genomics Resource Laboratory (CGRL), http://qb3.berkeley.edu/qb3/cgrl/
Computational Research Division at the Berkeley Lab , http://crd.lbl.gov/
DLab, http://dlab.berkeley.edu
Electronic Cultural Atlas Initiative (ECAI), http://www.ecai.org/
Energy Frontier Research Center (EFRC), http://www.cchem.berkeley.edu/co2efrc/
Experimental Social Science Laboratory (XLab), http://xlab.berkeley.edu/
Geospatial Innovation Facility, http://gif.berkeley.edu/
Geospatial Innovation Facility (GIF), http://gif.berkeley.edu/
Helen Wills Neuroscience Institute, http://neuroscience.berkeley.edu/
Henry H. Wheeler, Jr. Brain Imaging Center (BIC), http://bic.berkeley.edu/
i4Energy Center, http://i4energy.org/
Institute for Business Innovation, http://businessinnovation.berkeley.edu/data-science-strategy/
Joint BioEnergy Institute (JBEI), http://www.jbei.org/
Joint Genome Institute (JGI), http://www.jgi.doe.gov/
Molecular Foundry, http://foundry.lbl.gov/
NERSC, https://www.nersc.gov/
Nuclear Science and Security Consortium (NSSC), http://nssc.berkeley.edu/
Radio Astronomy Laboratory (RAL), http://vcresearch.berkeley.edu/research-unit/radio-astronomy-laboratory
Redwood Center for Theoretical Neuroscience, http://redwood.berkeley.edu/
Research IT, http://research-it.berkeley.edu/
Scalable Data Management, Analysis, and Visualization (SDAV), http://www.sdav-scidac.org/
SDAV, http://www.sdav-scidac.org/
Simons Institute, http://simons.berkeley.edu/
Space Sciences Laboratory (SSL), http://www.ssl.berkeley.edu/
Synthetic Biology Engineering Research Center (SYNBERC), http://synberc.org/
The Archaeological Research Facility, http://arf.berkeley.edu/
The Electronic Cultural Atlas Initiative, http://www.ecai.org/
Theoretical Astrophysics Center (TAC), http://astro.berkeley.edu/tac/
Townsend Center for the Humanities, http://townsendcenter.berkeley.edu/
Urban Analytics Lab, http://ual.berkeley.edu/
UrbanSim, http://www.urbansim.org/Main/WebHome
Visualization Group, http://vis.berkeley.edu/"""
