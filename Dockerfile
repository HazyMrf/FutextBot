FROM ubuntu:20.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.8

RUN apt-get install -y python3-pip

RUN pip install aiogram

COPY . .
CMD ["python3", "bot.py"]