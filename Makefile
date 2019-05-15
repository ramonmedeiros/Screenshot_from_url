VERSION=v10

default: run

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
	kubectl scale deployment hello-web --replicas 3
