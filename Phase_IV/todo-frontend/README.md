🚀 Full Stack Kubernetes Deployment: Step-by-Step Guide
Phase 1: Dockerization (The Foundation)
Before Kubernetes, we must turn the code into portable images.

Backend Image:

Navigate to the backend folder.

Create a Dockerfile using Python (FastAPI).

Build the image: docker build -t todo-backend:latest .

Frontend Image:

Navigate to the web folder.

Create a Dockerfile using Node.js (Next.js).

Crucial: Use --build-arg to inject the API URL so the browser knows where to send requests.

Build the image: docker build --build-arg NEXT_PUBLIC_API_URL=http://todo.test/api -t todo-frontend:latest .

Phase 2: Helm Chart Creation (The Blueprints)
Instead of manual YAML files, we use Helm to manage our application.

Create Charts:

Run helm create todo-backend and helm create todo-frontend.

Configure Templates:

Modify deployment.yaml in each chart to use your local images.

Set imagePullPolicy: IfNotPresent so Kubernetes looks for local images.

Service Setup:

Configure service.yaml for both. Frontend usually targets port 3000 (exposed on 80), and Backend targets 8000.

Phase 3: Initial Deployment & Verification
Before setting up complex networking, we verify the "brain" of the app works.

Start Minikube: minikube start --driver=docker

Load Images: Push your local images into the cluster:

PowerShell
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
Install Charts:

PowerShell
helm install todo-back ./todo-backend
helm install todo-front ./todo-frontend
Verify with Port-Forward:

Test Backend: kubectl port-forward svc/todo-back-todo-backend 8000:8000

Test Frontend: kubectl port-forward svc/todo-front-todo-frontend 3000:80

Confirmation: Ensure you can add a task via localhost:3000.

Phase 4: Secrets & Hardening
We move sensitive data out of the code and into Kubernetes.

Create Secret Manifest: Create app-secrets.yaml containing DATABASE_URL, AUTH_SECRET, and BETTER_AUTH_URL.

Apply Secrets: kubectl apply -f ./secrets/app-secrets.yaml

Update Deployments: Map these secrets to environment variables in your Helm templates so the pods can read them.

Phase 5: Ingress Routing (The Front Door)
This replaces Port-Forwarding with a professional domain name (todo.test).

Enable Ingress Controller: minikube addons enable ingress

Create Ingress File: Inside todo-frontend/templates/ingress.yaml, define the rules:

/api routes to the Backend Service.

/ routes to the Frontend Service.

Add Rewrite Annotation: nginx.ingress.kubernetes.io/rewrite-target: /$2

Apply Changes: helm upgrade todo-front ./todo-frontend

Phase 6: Windows Networking Bridge
Final steps to make http://todo.test work in your Chrome/Edge browser.

Patch the Controller: Force the Ingress to act as a LoadBalancer:

PowerShell
kubectl patch svc ingress-nginx-controller -n ingress-nginx -p '{\"spec\": {\"type\": \"LoadBalancer\"}}'
Hosts File: Edit C:\Windows\System32\drivers\etc\hosts (Admin mode) and add: 127.0.0.1 todo.test

Start the Tunnel: Run minikube tunnel --cleanup and enter password 1234 (configured via minikube ssh).

Summary of Final URLS
Application: http://todo.test

API Docs: http://todo.test/api/docs