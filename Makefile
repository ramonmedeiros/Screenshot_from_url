default: run

container:
	docker build src --tag=test-build 

run: container
	docker run --shm-size="512m" -e DBUS_SESSION_BUS_ADDRESS='/dev/null' -p 5000:5000 test-build

container-google:
	docker build -t gcr.io/detectify-challenge-ramon/hello-app:v4 src/
	docker push gcr.io/detectify-challenge-ramon/hello-app:v4

deploy:
	kubectl delete deployments,services hello-web
	kubectl create -f k8s/deployment.yaml
	kubectl create -f k8s/service.yaml
