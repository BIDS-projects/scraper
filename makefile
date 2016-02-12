LOGPATH = logs
LOGFILE = $(LOGPATH)/$(spider)-$(shell date +'%Y%m%d%H%M%S').log


check: check.sh
	bash check.sh

install: install.sh
	bash install.sh

deploy: ${path}/*
	cd ${path} && \
	shub deploy

crawl: ${project}/*
	cd ${project} && \
	[[ -d ${LOGPATH} ]] || mkdir ${LOGPATH} && \
	scrapy crawl ${spider}
	#scrapy crawl ${spider} --logfile=${LOGFILE}
