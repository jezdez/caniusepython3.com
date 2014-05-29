.PHONY: dev deploy

dev:
	foreman start

deploy:
	cd deploy; make deploy
