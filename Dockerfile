FROM python:3.10.2

WORKDIR /app
ADD ./requirements.txt ./requirements.txt
RUN pip install -U pip && pip install -r ./requirements.txt

COPY ./src ./src
COPY ./app.py ./app.py