FROM python:3.12.6-alpine3.20
WORKDIR /sanic
COPY . .
RUN pip install -r requirements/requirements.txt
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
