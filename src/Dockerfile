FROM python:3.11

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /home/discord_bot
WORKDIR /home/discord_bot

RUN pip install -r requirements.txt
EXPOSE 8443

CMD uvicorn run_bot:app --reload --port 8443 --host 0.0.0.0