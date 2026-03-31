FROM python:3.9-slim

RUN apt-get update && apt-get install -y stress-ng && apt-get clean

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"] 