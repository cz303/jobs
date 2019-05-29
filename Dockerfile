FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.pip /app/
RUN pip install -r requirements.pip
COPY . /app/