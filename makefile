check: check.sh
	bash check.sh

install: install.sh
	bash install.sh

deploy:
	source activate.sh &
		cd ${path} &
		shub deploy
