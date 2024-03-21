# syntax=docker/dockerfile:1

FROM python:3.9-slim

	
# Create app directory
WORKDIR /outlier

COPY . /outlier	

RUN pip install -r src/requirements.txt

EXPOSE 80

COPY . .

CMD [ "python3", "src/server.py"]
