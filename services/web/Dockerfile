# not pull official base image
# FROM python:3.8.0-alpine
# but from https://github.com/GeoBigData/geopandas-base
# geopandas-base:3.6

FROM python:3.6

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to
# disc (equivalent to python -B option)
#PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
# (equivalent to python -u option)

# Install the C compiler tools
RUN apt-get update -y && \
  apt-get install build-essential -y

RUN apt-get install -y --no-install-recommends apt-utils

# Install libspatialindex
WORKDIR /tmp

RUN wget http://download.osgeo.org/libspatialindex/spatialindex-src-1.8.5.tar.gz && \
  tar -xvzf spatialindex-src-1.8.5.tar.gz && \
  cd spatialindex-src-1.8.5 && \
  ./configure && \
  make && \
  make install && \
  cd - && \
  rm -rf spatialindex-src-1.8.5* && \
  ldconfig

WORKDIR /usr/src/app

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# w8t db up and running before creating db
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
