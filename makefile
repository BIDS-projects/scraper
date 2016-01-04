check: check.sh
	bash check.sh

install: install.sh
	bash install.sh

deploy: ${path}/*
	source activate.sh && \
		cd ${path} && \
		shub deploy

crawl: ${project}/*
	source activate.sh && \
	cd ${project} && \
	scrapy crawl ${spider}
