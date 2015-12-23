## Introduction
Crawls through websites of data science institutions and collect relevant information to aid DSI ecosystem mapping

## Installation

You will need `scrapy` installed. `pip install scrapy`

## Running

You can run the spider by running `scrapy crawl dlab` on `lab_relationship`
directory. `dlab` is specified under the `DlabSpider` class in `dlab.py`.

Once the spider finishes crawling, or whenever you close the spider (ctrl + c once; twice force quits which does not activate the persisting), it will store the results under `results.json`.
