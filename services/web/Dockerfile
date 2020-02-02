# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to
# disc (equivalent to python -B option)
#PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
# (equivalent to python -u option)


# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
# w8t db up and running before creating db
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
