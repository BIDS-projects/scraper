# Scraper

Generalized scraper for BIDS institutional ecosystem mapping. See below for types of spiders.

# Installation

Clone the repository.

```
git clone git@github.com:BIDS-projects/scraper
```

Setup your virtual environment. The following will create a new environment called `scraper`.

```
conda create -n scraper python=2.7
```

Activate your virtual environment, and install all dependencies from `requirements.txt`.

```
source activate scraper
pip install -r requirements.txt
```

Installation complete. See "How to Use" to get started.

# How to Use

Make sure to activate your virtual environment, if you haven't already. (If you are in the environment, your prompt will be prefixed by `(scraper)`)

```
source activate scraper
```

To run a spider, use the following, where `project` is the directory for your project, and `spider` is the name of the spider.

```
make crawl project=[project] spider=[spider]
```

See below for more information about each spider, and specific instructions for how to use each.

## Web Labs Raw

The raw spider saves raw HTML and a many-to-many connecting webpages with links. To launch `labs/labs/spiders/dlab.py`, use

```
make crawl project=labs/labs spider=weblabs
```

# Deployment

> Some sections are specific to BIDS IEM team members.

## ScrapingHub

Deploy using `make deploy path=[target]`, where `target` is the path to the
directory containing your spider.

## Production

You must have an account on Mercury, setup through BIDS IEM. SSH onto server.

```
ssh [username]@mercury.dlab.berkeley.edu
```

[More instructions coming soon]
