FROM python:3.8-alpine
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY producer.py /app/producer.py
#EXPOSE 5000
CMD ["python", "producer.py"]
