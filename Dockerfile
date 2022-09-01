FROM python:3.7.3-alpine3.9

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache --virtual .build-deps gcc musl-dev bash

WORKDIR /var/task
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apk del .build-deps



COPY ./src .
EXPOSE 8000
ENV AWS_DEFAULT_REGION=eu-west-1

ARG CLIENT_ID 
ENV CLIENT_ID=$CLIENT_ID

ARG CLIENT_SECRET
ENV CLIENT_SECRET=$CLIENT_SECRET 

ARG USER_POOL_ID
ENV USER_POOL_ID=$USER_POOL_ID 

CMD ["python", "server.py"]
