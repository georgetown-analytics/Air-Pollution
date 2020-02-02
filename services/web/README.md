**Docker Flask Postgres NGinx configuration**

 * From https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

 Follow this instruction to install and run:

 First make sure to have docker and docker-compose installed on your local computer : https://docs.docker.com/install/
 (Note no docker ce support for last ubuntu version, so I used the previous one like descried here : https://github.com/docker/for-linux/issues/833)

Maybe adapt version
version: '3.7' in the docker compose I used my version

after follow:

- sudo docker-compose build
- sudo docker-compose up -d
- [ sudo docker-compose exec web python manage.py create_db (created by entrypoint sh script) ]

to seed db (see method in manage.py) :

- sudo docker-compose exec web python manage.py seed_db

to connect and test db:

- sudo docker-compose exec db psql --username=airQuality --dbname=airQuality_dev
and then
 - \l  
 - \c airQuality_dev
 - \dt
 - select * from measure;
 - \q
