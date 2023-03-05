FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home
RUN apt update -y && apt install -y git nano curl
RUN git clone --branch dev https://github.com/mehmet-zahid/discord-bot.git

WORKDIR /home/discord-bot/src
RUN pip install -r requirements.txt

EXPOSE 8443
CMD git pull --ff-only origin && python3 bot.py