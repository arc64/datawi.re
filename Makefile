# DATAWIRE_SECRET = $(`DATAWIRE_SECRET`)

service:
	python datawire/manage.py createservice data/test_service.json

submit:
	curl -X POST -H 'Content-type: application/json' --data @data/test_frame.json "http://localhost:5000/api/1/frames/test/default?api_key=$(DATAWIRE_SECRET)"

web:
	python datawire/manage.py runserver