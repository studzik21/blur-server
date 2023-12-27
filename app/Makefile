username = studzik21

dep:
	poetry export -f requirements.txt  --without-hashes > requirements.txt

build:
	docker build  -t "$(username)/helloworld-python" .

run:
	docker run --env PORT=5000 -p 5000:5000 --env-file ../.env/.env $(username)/helloworld-python
