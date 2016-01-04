# -*- coding: utf-8 -*-
# PIPELINE: get a list of data science institutions and their websites -> crawl through each of the listed organization's internal links and aggregate external links -> save as HTML
from urlparse import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
import scrapy
import csv
import json

# DYNAMIC ITEM REFERNCE: (http://stackoverflow.com/questions/5069416/scraping-data-without-having-to-explicitly-define-each-field-to-be-scraped)
# Network Analysis Algorithms: https://networkx.github.io/documentation/latest/reference/algorithms.html

# TODO: fix the qb3 bug (if the seed url contains path, it fails)
# TODO: exit if you are on one path for too long (amplab, jenkins)

class MappingItem(dict, BaseItem):
    pass

# import os

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

class BareSpider(scrapy.Spider):
    name = "bare"

    def __init__(self, *args):
        item = MappingItem()
        self.loader = ItemLoader(item)
        self.filter_urls = list()

    def start_requests(self):
        try:
            reader = map(lambda x: x.split(','), seed.strip().split('\n'))
            for row in reader:
                seed_url = row[1].strip()
                base_url = urlparse(seed_url).netloc
                self.filter_urls.append(base_url)
                request = Request(seed_url, callback=self.parse_seed)
                request.meta['base_url'] = base_url
                #self.logger.info("'{}' REQUESTED".format(seed_url))
                yield request
        except IOError:
            raise CloseSpider("A list of websites are needed")

    def parse_seed(self, response):
        #self.logger.info("IN PARSE_SEED FOR {}".format(response.url))
        base_url = response.meta['base_url']
        # handle external redirect while still allowing internal redirect
        if urlparse(response.url).netloc != base_url:
            return
        external_le = LinkExtractor(deny_domains=base_url)
        external_links = external_le.extract_links(response)
        for external_link in external_links:
            if urlparse(external_link.url).netloc in self.filter_urls:
                self.loader.add_value(base_url, external_link.url)

        internal_le = LinkExtractor(allow_domains=base_url)
        internal_links = internal_le.extract_links(response)

        for internal_link in internal_links:
            request = Request(internal_link.url, callback=self.parse_seed)
            request.meta['base_url'] = base_url
            request.meta['dont_redirect'] = True
            yield request

    def get_external_links(self, base_url, response):
        pass

    def get_internal_links(self, base_url, response):
        pass

    def closed(self, reason):
        output = self.loader.load_item()
        self.logger.info("@@@@: {}".format(output))
        with open(self.output_filename, 'w') as outfile:
            json.dump(output, outfile, sort_keys=True, indent=4, separators=(',', ': '))
