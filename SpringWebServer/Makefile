#Make file for profile service

run: contain
	docker run --network my-network -p8090:8090 profile-service:latest

contain: build
	docker build --tag=profile-service:latest .

build: clean
	./gradlew build

clean:
	rm -r -f build