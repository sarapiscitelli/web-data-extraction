FROM python:3.11-slim-buster

# set environment variables
ARG SCRAPER_BACKEND_HOST
ENV SCRAPER_BACKEND_HOST=${SCRAPER_BACKEND_HOST}
ARG SCRAPER_BACKEND_PORT
ENV SCRAPER_BACKEND_PORT=${SCRAPER_BACKEND_PORT}

# add source code
RUN mkdir /app
WORKDIR /app
COPY src/ /app

# install requirements
RUN pip3 install -e .

#CMD tail -f /dev/null # keep container running for debugging purposes
CMD uvicorn backend.main:app --host $SCRAPER_BACKEND_HOST --port $SCRAPER_BACKEND_PORT
