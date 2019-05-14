default: run

container:
	docker build . --tag=test-build 

run: container
	docker run --shm-size="512m" -e DBUS_SESSION_BUS_ADDRESS='/dev/null' -p 5000:5000 test-build

