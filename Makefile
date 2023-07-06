build:
	@docker build \
		--build-arg INSTALL_DEV="1" \
		--progress plain \
		-t fastcookie:latest .

run:
	@docker run \
		--rm \
		-i \
		-v "$(shell pwd):/app" \
		--name fastcookie \
		fastcookie:latest

.PHONY: build run