FROM python:3.8-alpine
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY consumer.py /app/consumer.py
CMD ["python", "consumer.py"]