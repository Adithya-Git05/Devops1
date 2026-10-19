# Exercise 10 — Multi-Node Kubernetes and Multiple Applications

## Requirements

- Docker Desktop using Linux containers.
- Minikube and kubectl.
- Python and Docker to build the two Flask images.

Install the Python dependency and run the unit tests from this folder:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Create the cluster

Check `minikube profile list` first. If the `devops-multinode` profile does not
already exist, start the three-node cluster:

```powershell
minikube start --driver=docker --nodes=3 -p devops-multinode --kubernetes-version=v1.31.0
```

This pins the cluster to the Kubernetes version shown in the lab manual; Kubernetes
1.35.1 caused the control-plane kubelet to crash in this environment.

Do not delete an existing profile to make room; choose a different profile
name and use it consistently if necessary.

## Build and load both images

From this folder:

```powershell
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

## Deploy and verify replicas

```powershell
kubectl --context=devops-multinode apply -f product_catalog_deployment.yaml
kubectl --context=devops-multinode apply -f shopping_cart_deployment.yaml
kubectl --context=devops-multinode apply -f product_catalog_service.yaml
kubectl --context=devops-multinode apply -f shopping_cart_service.yaml
kubectl --context=devops-multinode get pods -o wide
```

The catalog must have two ready replicas on different nodes; the cart must
have three ready replicas on three different nodes.

## Test the services

In two separate terminals, start one service tunnel per command and leave each
terminal open:

```powershell
minikube -p devops-multinode service product-catalog-service --url
minikube -p devops-multinode service shopping-cart-service --url
```

Leave both commands running. In a third PowerShell terminal, paste the URLs
printed by those commands when prompted:

```powershell
$productUrl = Read-Host "Product Catalog URL"
$cartUrl = Read-Host "Shopping Cart URL"
Invoke-RestMethod "$productUrl/products"
Invoke-RestMethod "$cartUrl/cart"
Invoke-RestMethod -Method Post -Uri "$cartUrl/cart" `
  -ContentType "application/json" `
  -Body '{"id":1,"name":"Laptop","quantity":1}'
```

The product endpoint returns three products. The initial cart is empty, and
the POST returns the added item with HTTP 201.

Genuine screenshots captured from the deployed services are in `screenshots/`:
`product-catalog-response.png` and `shopping-cart-response.png`.
