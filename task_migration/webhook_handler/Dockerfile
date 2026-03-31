FROM python:3.9-slim

WORKDIR /app

COPY webhook_server.py .
COPY migrate_pod.py .
COPY deployment-edge.yaml .

RUN pip install flask

ENV KUBECTL_VERSION=v1.27.0
RUN apt-get update && apt-get install -y curl ca-certificates && \
    curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["python3", "webhook_server.py"]


