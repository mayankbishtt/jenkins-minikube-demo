# jenkins-minikube-demo
For something this detailed and reusable as long-term notes, I'll put it in a structured document format that you can save directly into your DevOps notes.

# End-to-End DevOps Project Notes

## Jenkins + GitHub + Docker + Kubernetes (Minikube) + JMeter

---

# 1. PROJECT OBJECTIVE

Build a complete CI/CD pipeline using:

* GitHub
* Jenkins
* Docker
* Kubernetes (Minikube)
* JMeter

Goal:

```text
Developer
    ↓
GitHub
    ↓
Jenkins
    ↓
Docker Build
    ↓
Minikube
    ↓
Kubernetes Deployment
    ↓
JMeter Performance Testing
```

---

# 2. FINAL ARCHITECTURE

```text
                 ┌──────────────┐
                 │   GitHub     │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   Jenkins    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Docker Build │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  Minikube    │
                 │ Kubernetes   │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │ Flask App    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   JMeter     │
                 └──────────────┘
```

---

# 3. TOOLS USED

## GitHub

Purpose:

* Source Code Management
* Version Control
* Repository Hosting

Repository contains:

```text
app.py
Dockerfile
requirements.txt
k8s/
jmeter/
```

---

## Jenkins

Purpose:

* Continuous Integration
* Build Automation
* Deployment Automation

Responsibilities:

```text
Pull code
Build Docker Image
Load image to Minikube
Deploy to Kubernetes
Run JMeter
Generate Reports
```

---

## Docker

Purpose:

Package application into a portable image.

Command:

```powershell
docker build -t flask-demo:version1 .
```

Verify:

```powershell
docker images
```

---

## Kubernetes (Minikube)

Purpose:

Run and manage containers.

Concepts used:

```text
Deployment
ReplicaSet
Pod
Service
NodePort
```

---

## JMeter

Purpose:

Performance Testing

Measures:

```text
Response Time
Throughput
Error %
Latency
```

---

# 4. PROJECT STRUCTURE

```text
jenkins-minikube-demo

│
├── app.py
├── Dockerfile
├── requirements.txt
│
├── k8s
│   ├── deployment.yaml
│   └── service.yaml
│
└── jmeter
    └── flask-load-test.jmx
```

---

# 5. FLASK APPLICATION

app.py

```

Purpose:

```text
Simple application to deploy on Kubernetes.
```

---

# 6. REQUIREMENTS FILE

requirements.txt

```text
flask
```

Install:

```powershell
python -m pip install flask
```

---

# 7. DOCKERFILE



# 8. TEST APPLICATION LOCALLY

Navigate:

```powershell
cd C:\Users\mayan\Desktop\jenkins-minikube-demo
```

Run:

```powershell
python app.py
```

Open:

```text
http://localhost:5000
```

Output:

```text
Hello from Jenkins and Kubernetes
```

---

# 9. BUILD IMAGE

```powershell
docker build -t flask-demo:version1 .
```

Verify:

```powershell
docker images
```

---

# 10. START KUBERNETES

Check:

```powershell
minikube status
```

Start:

```powershell
minikube start
```

Verify:

```powershell
kubectl get nodes
```

Expected:

```text
Ready
```

---

# 11. DEPLOYMENT.YAML

```yaml

---

# 12. SERVICE.YAML

```yaml


---

# 13. DEPLOY APPLICATION

```powershell
kubectl apply -f k8s/
```

Verify:

```powershell
kubectl get deployments
```

```powershell
kubectl get pods
```

```powershell
kubectl get svc
```

---

# 14. FIRST MAJOR ERROR

Error:

```text
ErrImageNeverPull
```

Command:

```powershell
kubectl describe pod <pod-name>
```

Output:

```text
Container image "flask-demo:version1" is not present with pull policy of Never
```

Reason:

```text
Image existed in Docker Desktop

Image did NOT exist inside Minikube
```

---

# 15. FIX FOR ErrImageNeverPull

Command:

```powershell
minikube image load flask-demo:version1
```

Restart:

```powershell
kubectl rollout restart deployment flask-app
```

Verify:

```powershell
kubectl get pods
```

Expected:

```text
Running
```

---

# 16. JENKINS SETUP

Start Jenkins:

```powershell
java -jar jenkins.war
```

Open:

```text
http://localhost:8080
```

---

# 17. GITHUB AUTHENTICATION

Repository:

```text
Private Repository
```

Used:

```text
GitHub PAT
```

Configured in:

```text
Manage Jenkins
↓
Credentials
```

Credential ID:

```text
github-pat
```

---

# 18. JENKINS PIPELINE

```groovy
pipeline {


}
```

---

# 19. ACCESS APPLICATION

Get URL:

```powershell
minikube service flask-service --url
```

Open URL.

---

# 20. LOGGING

Check Pods:

```powershell
kubectl get pods
```

Logs:

```powershell
kubectl logs <pod-name>
```

Live Logs:

```powershell
kubectl logs -f <pod-name>
```

---

# 21. WHY LOGS WERE EMPTY

Reason:

```python
return "Hello from Jenkins and Kubernetes"
```

This is:

```text
HTTP Response
```

NOT:

```text
Application Log
```

Added:

```python
print("Application Started")
```

and

```python
print("Request received", flush=True)
```

Logs started appearing.

---

# 22. JMETER SETUP

Created:

```text
flask-load-test.jmx
```

Thread Group:

```text
Threads = 10
Ramp-Up = 5
Loop Count = 10
```

Total Requests:

```text
100
```
C:\Users\mayan\Downloads\apache-jmeter-5.6.3\bin>jmeter -n ^
More? -t C:\Users\mayan\Desktop\jenkins-minikube-demo\jmeter\flask-load-test.jmx ^
More? -l results.jtl

used to create a jtl file locally and then push that file in github and then change the port according to your need evrytime you run a new build. this is done manually now.
---

# 23. RUN JMETER MANUALLY

```powershell
jmeter -n -t flask-load-test.jmx -l results.jtl
```

Output:

```text
summary = 100 requests

Avg = 77ms

Err = 0%
```

---

# 24. GENERATE REPORT

```powershell
jmeter -g results.jtl -o report
```

Generated:

```text
report/
    index.html
```

---

# 25. JENKINS + JMETER

Added:

```groovy
stage('Performance Test') {
    steps {
        bat '''
        if exist results.jtl del results.jtl

        "C:\\Users\\mayan\\Downloads\\apache-jmeter-5.6.3\\bin\\jmeter.bat" -n -t jmeter\\flask-load-test.jmx -l results.jtl
        '''
    }
}

stage('Generate Report') {
    steps {
        bat '''
        if exist report rmdir /s /q report

        "C:\\Users\\mayan\\Downloads\\apache-jmeter-5.6.3\\bin\\jmeter.bat" -g results.jtl -o report
        '''
    }
}
```

---

# 26. SECOND MAJOR ERROR

Error:

```text
'jmeter' is not recognized
```

Reason:

```text
Jenkins could not find jmeter.bat
```

Fix:

Used full path:

```text
C:\Users\mayan\Downloads\apache-jmeter-5.6.3\bin\jmeter.bat
```

---

# 27. THIRD MAJOR ERROR

Error:

```text
Duplicate options for -n
```

Reason:

Pipeline contained:

```text
-n
jmeter -n
```

Two -n flags.

Fix:

```text
Keep only one -n
```

---

# 28. FOURTH MAJOR ERROR

JMeter showed:

```text
50% Pass
50% Fail
```

Investigation:

Application code was correct.

Root Cause:

```text
Old results.jtl file existed

Old report folder existed

New data mixed with old data
```

Fix:

Delete:

```powershell
results.jtl
```

and

```powershell
report
```

before every run.

---

# 29. IMPORTANT KUBERNETES COMMANDS

Pods:

```powershell
kubectl get pods
```

Deployments:

```powershell
kubectl get deployments
```

Services:

```powershell
kubectl get svc
```

Logs:

```powershell
kubectl logs <pod>
```

Live Logs:

```powershell
kubectl logs -f <pod>
```

Describe Pod:

```powershell
kubectl describe pod <pod>
```

Restart Deployment:

```powershell
kubectl rollout restart deployment flask-app
```

Endpoints:

```powershell
kubectl get endpoints
```

---

# 30. CRASHLOOPBACKOFF NOTES

Meaning:

```text
Container Starts
↓
Container Crashes
↓
Kubernetes Restarts
↓
Container Crashes Again
↓
CrashLoopBackOff
```

Troubleshooting:

```powershell
kubectl logs <pod>
```

```powershell
kubectl describe pod <pod>
```

---

# 31. DEVOPS CONCEPTS LEARNED

GitHub:

* Version Control

Jenkins:

* CI
* Pipeline

Docker:

* Images
* Containers

Kubernetes:

* Pods
* Deployments
* Services
* ReplicaSets

JMeter:

* Performance Testing
* Throughput
* Error Rate
* Response Time

Troubleshooting:

* kubectl logs
* kubectl describe
* JMeter Reports

---

# 32. FINAL LEARNING OUTCOME

Successfully built:

```text
GitHub
↓
Jenkins
↓
Docker Build
↓
Minikube Image Load
↓
Kubernetes Deployment
↓
Application Access
↓
JMeter Performance Testing
↓
HTML Report Generation
```