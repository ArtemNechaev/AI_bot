FROM python:3.10

COPY ./app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install --upgrade pip -r requirements.txt
COPY ./app /app

CMD ["python3", "bot.py"]