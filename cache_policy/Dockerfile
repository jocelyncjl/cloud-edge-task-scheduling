FROM python:3.9-slim

WORKDIR /app

COPY product_service.py .

RUN pip install flask

CMD ["python3", "product_service.py"]