FROM python:3.11.3

WORKDIR /dcrm

COPY . /dcrm

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
