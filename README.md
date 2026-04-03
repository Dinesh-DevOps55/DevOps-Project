# Cloud-Native DevOps Demo (Flask + Docker + EKS)

Minimal microservices project showing a real DevOps workflow:
- Two Python Flask services (`user-service`, `product-service`)
- Dockerized services
- Kubernetes manifests (EKS-compatible)
- GitHub Actions CI/CD to ECR + EKS
- Terraform for ECR + EKS infrastructure
- Optional Prometheus setup

## Project Structure

```text
.
|-- .github/
|   `-- workflows/
|       `-- cicd.yaml
|-- k8s/
|   |-- namespace.yaml
|   |-- user-service-deployment.yaml
|   |-- user-service-service.yaml
|   |-- product-service-deployment.yaml
|   |-- product-service-service.yaml
|   `-- monitoring/
|       |-- prometheus-configmap.yaml
|       |-- prometheus-deployment.yaml
|       `-- prometheus-service.yaml
|-- product-service/
|   |-- app.py
|   |-- requirements.txt
|   |-- Dockerfile
|   `-- .dockerignore
|-- terraform/
|   |-- providers.tf
|   |-- variables.tf
|   |-- main.tf
|   |-- outputs.tf
|   `-- terraform.tfvars.example
`-- user-service/
    |-- app.py
    |-- requirements.txt
    |-- Dockerfile
    `-- .dockerignore
```

## 1) Prerequisites

- Python 3.11+ (or 3.12 recommended)
- Docker Desktop
- `kubectl`
- AWS CLI configured (`aws configure`)
- Terraform (`>= 1.5`)
- GitHub repository with Actions enabled

## 2) Run Services Locally (without Docker)

### user-service

```bash
cd user-service
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
python app.py
```

Test:

```bash
curl http://localhost:5000/users
curl http://localhost:5000/healthz
```

### product-service

```bash
cd product-service
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
python app.py
```

Test:

```bash
curl http://localhost:5001/products
curl http://localhost:5001/healthz
```

## 3) Run with Docker

From repo root:

```bash
docker build -t user-service:local ./user-service
docker build -t product-service:local ./product-service

docker run -d --name user-service -p 5000:5000 user-service:local
docker run -d --name product-service -p 5001:5001 product-service:local
```

Test:

```bash
curl http://localhost:5000/users
curl http://localhost:5001/products
```

## 4) Provision AWS Infrastructure with Terraform

From `terraform/`:

```bash
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply -auto-approve
```

After apply:

```bash
aws eks update-kubeconfig --name devops-demo-eks --region us-east-1
kubectl get nodes
```

## 5) Deploy to Kubernetes (Manual)

From repo root:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/user-service-deployment.yaml
kubectl apply -f k8s/user-service-service.yaml
kubectl apply -f k8s/product-service-deployment.yaml
kubectl apply -f k8s/product-service-service.yaml
```

Check:

```bash
kubectl -n devops-demo get pods
kubectl -n devops-demo get svc
```

Notes:
- Deployment manifests start with placeholder images (`example.com/...`).
- In production, CI/CD updates image tags automatically via `kubectl set image`.

## 6) Optional Prometheus Deployment

```bash
kubectl apply -f k8s/monitoring/prometheus-configmap.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml
kubectl apply -f k8s/monitoring/prometheus-service.yaml
kubectl -n devops-demo get svc prometheus
```

Access Prometheus through NodePort `30090` on a worker node public IP (or port-forward).

## 7) GitHub Actions CI/CD Setup

Workflow file: `.github/workflows/cicd.yaml`

On push to `main`, pipeline:
1. Builds Docker images for both services
2. Pushes them to Amazon ECR
3. Applies Kubernetes manifests
4. Updates deployments to the new image tag (`github.sha`)
5. Waits for rollout success

### Required GitHub Secrets

Set these in your repository settings:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

The IAM user/role used by these keys needs permissions for:
- ECR push/pull
- EKS describe cluster
- Kubernetes deployment access (through EKS auth mapping)

## 8) Useful Commands

```bash
# Show cluster workloads
kubectl -n devops-demo get all

# Check service logs
kubectl -n devops-demo logs deploy/user-service
kubectl -n devops-demo logs deploy/product-service

# Restart deployments
kubectl -n devops-demo rollout restart deploy/user-service
kubectl -n devops-demo rollout restart deploy/product-service
```

## 9) DevOps Best Practices Included

- Small container base image (`python:3.12-slim`)
- Non-root container user
- Layered Docker build for better caching
- Readiness/liveness probes in Kubernetes
- Resource requests/limits in deployments
- Namespaced resources with labels
- Immutable image tagging in CI (`github.sha`)
- Infrastructure as Code via Terraform

