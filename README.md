## Introduction

Crawls through websites of data science institutions and collect relevant information to aid DSI ecosystem mapping

## Installation

Check that Python2.7 is installed using `make check`. Then, run the installation using `make install`.

To activate the virtual environment, use `source activate.sh`.

## Running

To run a spider, use `make crawl project=[project] spider=[spider]` where
`project` is the directory for your project, and `spider` is the name
of the spider.

For example, to launch `labs/labs/spiders/dlab.py`, use
`make crawl project=labs spider=weblabs`.

Once the spider finishes crawling, or whenever you close the spider (ctrl + c once; twice force quits which does not activate the persisting), it will store the results into the database.

## Deployment

Deploy using `make deploy path=[target]`, where `target` is the path to the
directory containing your spider.
