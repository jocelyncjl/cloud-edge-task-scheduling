# Rule-Based Task Scheduling in Cloud-Edge Computing
This repository contains an experimental implementation of a rule-based task scheduling system for cloud-edge computing. The project investigates how simple scheduling rules can improve resource utilization and reduce CPU pressure by deciding whether tasks should be processed in the cloud or at the edge.

The system is implemented on Kubernetes and combines Flask services, Docker containers, Istio traffic management, Prometheus monitoring, Alertmanager-based triggering, and Grafana dashboards. Instead of using machine learning or reinforcement learning, this project focuses on a lightweight rule-based approach that is easier to understand, deploy, and evaluate in resource-constrained environments.

## Project Objective
The goal of this project is to evaluate whether simple rule-based scheduling strategies can improve resource management and support energy-efficient cloud-edge cooperation.

The scheduling logic is based on system metrics such as CPU usage, memory usage, request patterns, and routing conditions. Depending on these metrics, the system applies predefined rules to:

- migrate workloads from cloud to edge when cloud CPU becomes too high
- route requests to edge nodes based on user location
- cache hot content closer to users
- scale cloud-side workloads by increasing Pod replicas under CPU pressure

## Research Scope
This project is aligned with the following four scheduling rules:
- R1: Task Migration
    Move workloads from cloud to edge when the cloud becomes overloaded.
- R2: Location-Aware Load Balancing
    Route requests to edge or cloud based on user location.
- R3: Cache Policy
    Send hot-content requests to edge-side services.
- R4: Cloud Scheduling with HPA
    Scale cloud-side application Pods when CPU utilization increases.

## Repository Structure
```text
task_scheduling_research/
├── load_balancing/                  # R2: location-aware routing
├── cache_policy/                    # R3: hot-content cache policy
├── cloud_scheduling/                # R4: HPA-based pod scaling
├── task_migration/                  # R1: alert-driven task migration
│   └── webhook_handler/        
└── README.md
```

System Architecture

The project uses a simple cloud-edge cluster model built on Kubernetes.
Main components:
- Cloud node
Hosts default or compute-heavy workloads.
- Edge node
Hosts latency-sensitive or migrated workloads.
- Pods
The basic Kubernetes execution unit used to run the services.
- Flask services
Simple application services used to simulate workloads and requests.
- Istio Gateway / VirtualService / DestinationRule
Used for traffic ingress, routing, and service subset selection.
- Prometheus
Collects metrics such as CPU and memory usage.
- Alertmanager
Sends alerts when thresholds are exceeded.
- Grafana
Visualizes CPU and resource behavior during the experiments.
- Webhook handler
Receives alerts and triggers migration actions.

Environment Setup

The experiments are designed to run on a local Kubernetes environment using Minikube.
Recommended setup:
- at least 4 CPU cores
- at least 8 GB memory
- Docker Desktop installed
- kubectl installed
- Minikube installed
- Helm installed
- Prometheus and Grafana deployed into the cluster

Example cluster creation:
```bash
minikube start --cpus=4 --memory=8192mb --nodes=2
kubectl label node minikube node-role=cloud
kubectl label node minikube-m02 edge-node=true
kubectl get nodes --show-labels
```

Monitoring Stack

The monitoring workflow is based on Prometheus and Grafana.
Prometheus collects:
- CPU usage
- workload activity
- service behavior during experiments

Grafana visualizes:
- cloud CPU trends
- migration and scaling effects over time

This monitoring setup is central to the evaluation, especially for comparing CPU behavior before and after migration, routing, caching, or scaling actions.

Experiment Modules

1. R1 Task Migration
Directory: task_migration/
This experiment evaluates workload migration from the cloud node to the edge node when the cloud-side CPU usage becomes too high.

Workflow:
- A Flask service runs on the cloud side
- A compute-heavy request increases CPU load
- Prometheus monitors cloud CPU usage
- When the configured CPU threshold is exceeded, an alert is triggered
- Alertmanager sends the alert to a webhook service
- The webhook runs a migration script
- The cloud-side Deployment is removed and the edge-side Deployment is applied

Purpose:
- reduce cloud-side CPU pressure
- demonstrate alert-driven workload relocation
- validate a simple rule-based control loop

Metrics and Evaluation:
Prometheus and Grafana are used to compare CPU behavior before and after migration.
Key comparison focus:
- cloud CPU usage before migration
- cloud CPU usage after the workload is removed

2. R2 Load Balancing
Directory: load_balancing/
This experiment evaluates location-aware traffic routing using Istio.

Workflow:
- requests enter through an Istio Gateway
- traffic is matched by header rules
- requests from a specific region are routed to the edge subset
- all other traffic is routed to the cloud subset

Purpose:
- reduce latency for nearby users
- distribute load based on request origin
- test rule-based traffic placement between cloud and edge

Metrics and Evaluation:
Prometheus and Grafana are used to compare CPU distribution across edge and cloud during traffic routing.
Key comparison focus:
- cloud CPU usage before and after location-based routing

3. R3 Cache Policy
Directory: cache_policy/
This experiment evaluates a simple hot-content scheduling strategy.
A product service is deployed to both cloud and edge. Requests for a specific hot product are routed to edge, while other requests are handled by the cloud. In the current implementation, hot-content routing is based on product ID 101.

Workflow:
- A user sends a request for a product page
- The request enters the system through the Istio Gateway
- Istio checks the request URI
- If the request matches the hot product path, such as `/product/101`, it is routed to the edge-side service
- If the request is for a normal product, it is routed to the cloud-side service
- Prometheus and Grafana can be used to observe how hot-content routing affects CPU usage on the cloud sides

Purpose:
- keep popular content closer to users
- reduce repeated cloud-side processing

Metrics and Evaluation:
Prometheus and Grafana are used to compare CPU impact under hot-content and non-hot-content request patterns.
Key comparison focus:
- cloud CPU usage before and after hot-content routing

4. R4 Cloud Scheduling
Directory: cloud_scheduling/
This experiment evaluates Kubernetes Horizontal Pod Autoscaler (HPA) as a rule-based scaling mechanism for cloud-side workloads.

Workflow:
- a service generates synthetic CPU load
- Prometheus metrics reflect increasing resource usage
- HPA watches CPU utilization
- when the threshold is exceeded, Kubernetes increases the number of Pod replicas in the target Deployment

Purpose:
- demonstrate CPU-driven autoscaling
- reduce overload by adding more application Pods
- evaluate rule-based elastic scaling in the cloud

Metrics and Evaluation:
Prometheus and Grafana are used to compare CPU behavior before and after scaling out.
Key comparison focus:
- CPU utilization before HPA activation
- CPU utilization after additional Pod replicas are created

Build Images

Build the Docker images for each module before deployment.
Examples:
```bash
cd task_migration
docker build -t flask-tasks-service:latest .

cd task_migration/webhook_handler
docker build -t webhook-handler:latest .

cd cache_policy
docker build -t product-service:latest .

cd cloud_scheduling
docker build -t scale-service:latest .
```

Deploy Monitoring

Prometheus and Grafana can be installed using Helm.
```bash 
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
kubectl create namespace monitoring
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring
```

Access Grafana:
```bash
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```

Deployment

R1 Task Migration
```bash
kubectl apply -f task_migration/deployment-cloud.yaml
kubectl apply -f task_migration/service-cloud.yaml
kubectl apply -f task_migration/webhook-rbac.yaml
kubectl apply -f task_migration/webhook-deploy.yaml
kubectl apply -f task_migration/prometheus-config.yaml
kubectl apply -f task_migration/prometheus-alertmanager.yaml
```

R2 Load Balancing
```bash
kubectl apply -f load_balancing/deployment-edge-lb.yaml
kubectl apply -f load_balancing/deployment-cloud-lb.yaml
kubectl apply -f load_balancing/service-lb.yaml
kubectl apply -f load_balancing/gateway.yaml
kubectl apply -f load_balancing/destination-rule.yaml
kubectl apply -f load_balancing/virtual-service.yaml
```

R3 Cache Policy
```bash
kubectl apply -f cache_policy/deployment-edge-cp.yaml
kubectl apply -f cache_policy/deployment-cloud-cp.yaml
kubectl apply -f cache_policy/service-cp.yaml
kubectl apply -f cache_policy/gateway-cp.yaml
kubectl apply -f cache_policy/destination-rule-cp.yaml
kubectl apply -f cache_policy/virtual-service-cp.yaml
```

R4 Cloud Scheduling
```bash
kubectl apply -f cloud_scheduling/deployment-cloud-cs.yaml
kubectl apply -f cloud_scheduling/deployment-edge-cs.yaml
kubectl apply -f cloud_scheduling/service-cpu-load.yaml
kubectl apply -f cloud_scheduling/scale-gateway.yaml
kubectl apply -f cloud_scheduling/destination-rule-cs.yaml
kubectl apply -f cloud_scheduling/virtual-service-cs.yaml
kubectl apply -f cloud_scheduling/hpa-scale.yaml
```

How to Test

R1 Task Migration Test

Trigger the compute-heavy workload:
```bash
curl http://<service-address>/compute-heavy
```
Observe the system:
```bash
kubectl get pods -w
kubectl get deployments
kubectl logs deployment/webhook-handler
```
Also check the Prometheus web UI and Grafana dashboards.
Expected result:
- cloud CPU usage increases under the compute-heavy task
- after migration, cloud CPU pressure decreases and edge-side CPU activity increases

R2 Load Balancing Test

Send requests with and without the location header:
```bash
curl -H "x-user-location: US" http://<gateway-address>/
curl http://<gateway-address>/
```
Expected result:
- requests with x-user-location: US are routed to edge-side Pods
- other requests are routed to cloud-side Pods

R3 Cache Policy Test

Request a hot product and a normal product:
```bash
curl http://<gateway-address>/product/101
curl http://<gateway-address>/product/102
```
Expected result:
- requests for product 101 go to edge-side Pods
- other product requests go to cloud-side Pods

R4 Cloud Scheduling Test

Start the synthetic load:
```bash
curl http://<gateway-address>/start
```
Monitor the scaling behavior:
```bash
kubectl get hpa
kubectl describe hpa scale-hpa
kubectl get pods -w
```
Expected result:
- CPU usage of the cloud-side application increases
- after scaling out, CPU pressure should be shared across more Pods

Evaluation Focus

The main evaluation metrics used in this project are: CPU usage, Special attention is given to CPU metrics, since the main scheduling rules are triggered by CPU pressure or designed to reduce CPU concentration on the cloud side. For task migration, the key comparison is: before scheduler: cloud CPU remains high, around 50-55%, after scheduler: cloud CPU drops to around 20-25%. This CPU reduction is the clearest evidence that the rule-based scheduler improves workload placement.



