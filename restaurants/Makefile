generate_containers:
	@docker build -t restaurants .
	@docker stop restaurantscontainer || true
	@docker rm restaurantscontainer || true
	@docker run -d --name restaurantscontainer -p 8000:8000 restaurants