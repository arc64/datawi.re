BOWER=node_modules/bower/bin/bower

web:
	python datawire/manage.py runserver

assets: frontend/node_modules frontend/bower_components
	cd frontend && grunt

watch: assets
	cd frontend && grunt watch

frontend/node_modules:
	cd frontend && npm install --dev

frontend/bower_components: frontend/node_modules
	cd frontend && $(BOWER) install

clean-deps:
	rm -rf frontend/node_modules
	rm -rf frontend/bower_components

clean:
	rm -f frontend/dist/*
