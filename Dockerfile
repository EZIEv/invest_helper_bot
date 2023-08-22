FROM python:bullseye
LABEL maintainer="samuilov2003@gmail.com"

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /invest_bot

COPY . .

RUN pip install -r requirements.txt

CMD python bot.py & python news.py