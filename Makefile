VERSION=v20
PROJECT=ramon-tests
TOPIC=queue
BUCKET=ramon_screenshots
default: run

tests:
	PYTHONPATH=src python -m unittest discover -v src/tests

set-local-vars:
	export -a GCS_BUCKET=$(BUCKET)
	export -a GCP_PROJECT=$(PROJECT)
	export -a GCP_TOPIC=$(TOPIC)

create-topic: set-local-vars
	python -c "from google.cloud import pubsub_v1;pubsub_v1.PublisherClient().create_topic('projects/$(PROJECT)/topics/$(TOPIC)')"

local-pub-sub:
	gcloud beta emulators pubsub --project=$(PROJECT) start

container:
	docker build src --tag=test-build 

run: container
	docker run --shm-size="512m" -e DBUS_SESSION_BUS_ADDRESS='/dev/null' -p 5000:5000 test-build

container-google:
	docker build -t gcr.io/detectify-challenge-ramon/hello-app:$(VERSION) src/
	docker push gcr.io/detectify-challenge-ramon/hello-app:$(VERSION)

deploy:
	kubectl delete deployments hello-web
	kubectl create -f k8s/deployment.yaml
	kubectl scale deployment hello-web --replicas 6
