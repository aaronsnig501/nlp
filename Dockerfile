FROM sanicframework/sanic:3.8-latest
WORKDIR /sanic
COPY . .
RUN pip install -r requirements/requirements.txt
EXPOSE 8000
CMD ["python", "server.py"]
