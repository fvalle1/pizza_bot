FROM python:alpine3.18

COPY requirements.txt /home/requirements.txt
RUN python3 -m pip install --no-cache-dir -U -r /home/requirements.txt


COPY pizza_bot.py /home/
COPY white_backend.py /home/
WORKDIR /home/

ENTRYPOINT python3 pizza_bot.py
