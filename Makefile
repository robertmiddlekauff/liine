generate_backend_containers:
	@docker build -t restaurants .
	@docker stop restaurantscontainer || true
	@docker rm restaurantscontainer || true
	@docker run -d --name restaurantscontainer -p 8000:8000 restaurants

build_app:
	@docker-compose build
	@docker-compose up