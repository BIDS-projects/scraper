## Introduction
Crawls through websites of data science institutions and collect relevant information to aid DSI ecosystem mapping

## Installation

Check that Python2.7 is installed using `make check`. Then, run the installation using `make install`.

In case the installation script fails, you may execute the contents of the bash script line by line:

1. Setup a new virtual environment: `python2.7 -m virtualenv env`.
1. Start the virtual environment: `source env/bin/activate`.
1. Install all requirements `pip install -r requirements.txt`.

> To activate the virtualenv, use `source activate.sh`.

## Running

You can run the spider by running `scrapy crawl dlab` on `lab_relationship`
directory. `dlab` is specified under the `DlabSpider` class in `dlab.py`.

Once the spider finishes crawling, or whenever you close the spider (ctrl + c once; twice force quits which does not activate the persisting), it will store the results under `results.json`.

## Deployment

Deploy using `make deploy path=[target]`, where `target` is the path to the
directory containing your spider.

In case the installation script fails, you may execute the contents of the bash script line by line:

1. Activate the virtual environment `source activate.sh`.
1. Navigate to the spider's directory `cd <spider>`.
1. Deploy using `shub deploy`.
