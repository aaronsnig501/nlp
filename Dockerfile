FROM python:3.12.6-alpine3.20
RUN apk add build-base
WORKDIR /sanic
COPY . .
RUN pip install -r requirements/requirements.txt
EXPOSE 80
CMD ["sanic", "server:app", "--host=0.0.0.0", "--port=80", "--workers=4"]
