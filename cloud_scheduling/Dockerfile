FROM python:3.9-slim

WORKDIR /app

RUN pip install flask

COPY scale_service.py .

CMD ["python3", "scale_service.py"]
