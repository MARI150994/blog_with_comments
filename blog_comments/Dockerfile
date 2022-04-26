FROM python:3.8-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install psycopg2 dependencies
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./prestart.sh .
RUN chmod +x prestart.sh


# copy project
COPY . .

ENTRYPOINT ["bash", "prestart.sh"]