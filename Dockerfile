# start by pulling the python image
FROM python:3.10-alpine

# switch working directory
WORKDIR /home/projects/BookEx

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /home/projects/BookEx/requirements.txt
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /home/projects/BookEx
