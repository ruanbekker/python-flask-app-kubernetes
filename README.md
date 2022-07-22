# flask-app-kubernetes

Deploy Python Flask app to Kubernetes (k3d)

## About

This project is a demonstration how to build, test and run a [Python Flask](https://flask.palletsprojects.com/en/2.1.x/) application locally using [docker-compose](https://docs.docker.com/get-started/08_using_compose/), then provision a local [Kubernetes](https://kubernetes.io/docs/home/) cluster using [K3d](https://k3d.io/stable/) which runs a lightweight kubernetes distribution called [K3s](https://k3s.io/) on [Docker](https://docs.docker.com/get-docker/).

I've included 2 methods to deploy k3d, either with the k3d binary or using [Terraform](https://www.terraform.io/) with the [terraform k3d provider](https://registry.terraform.io/providers/pvotal-tech/k3d/latest).

The config included uses 3 replicas for the python flask application, which is a basic application that returns the hostname of the runtime it runs on, and when it's deployed to the 3 node kubernetes cluster, we will test it by making 3 requests, and the traffic will be round-robin'd so we should see 3 different responses.

## Dependencies

The following is required:

- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/get-started/08_using_compose/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [terraform](https://www.terraform.io/)
- [k3d](https://k3d.io/stable/)

## Build and Run Locally

Build the application locally:

```
$ docker-compose up -d --build
```

Test locally:

```
$ curl http://localhost:8080/hostname
hello from 32c76a0d3784
```

View the logs locally:

```
$ docker-compose logs -f
Attaching to flask-app
flask-app    | [2022-06-04 23:04:59 +0000] [8] [INFO] Starting gunicorn 20.0.4
flask-app    | [2022-06-04 23:04:59 +0000] [8] [INFO] Listening at: http://0.0.0.0:8080 (8)
flask-app    | [2022-06-04 23:04:59 +0000] [8] [INFO] Using worker: threads
flask-app    | [2022-06-04 23:04:59 +0000] [10] [INFO] Booting worker with pid: 10
flask-app    | [2022-06-04 23:04:59 +0000] [11] [INFO] Booting worker with pid: 11
flask-app    | 172.19.0.1 - - [04/Jun/2022:23:05:13 +0000] "GET /hostname HTTP/1.1" 200 23 "-" "curl/7.54.0"
```

Terminate the application locally:

```
$ docker-compose down
Stopping flask-app ... done
Removing flask-app ... done
```

## Build and Push Container Image

Builld and push the images to your registry:

```
$ docker-compose build
$ docker-compose push
```

## Kubernetes

Provision a Kubernetes cluster either via [k3d](https://k3d.io/) or [terraform](https://www.terraform.io/)

### Kubernetes Cluster Option 1: Using k3d directly

Create a k3d (kubernetes on docker using k3s) kubernetes cluster:

```
$ k3d cluster create --config k3d-cluster.yml
INFO[0061] Cluster 'kubernetes-cluster' created successfully!
```

### Kubernetes Cluster Option 2: Using terraform

Create the k3d Kubernetes cluster with terraform:

```
terraform -chdir=infra init
terraform -chdir=infra plan
terraform -chdir=infra apply -auto-approve
```

Configuration such as the [k3s version](https://hub.docker.com/r/rancher/k3s/tags) can be configured under `./infra/variables.tf`.

## Overview of our Infrastructure

Check if the nodes are visible:

```
$ kubectl get nodes --output wide
NAME                              STATUS   ROLES                  AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE   KERNEL-VERSION     CONTAINER-RUNTIME
k3d-kubernetes-cluster-agent-0    Ready    <none>                 78s   v1.20.4+k3s1   172.20.0.4    <none>        Unknown    5.10.25-linuxkit   containerd://1.4.3-k3s3
k3d-kubernetes-cluster-agent-1    Ready    <none>                 77s   v1.20.4+k3s1   172.20.0.5    <none>        Unknown    5.10.25-linuxkit   containerd://1.4.3-k3s3
k3d-kubernetes-cluster-server-0   Ready    control-plane,master   99s   v1.20.4+k3s1   172.20.0.3    <none>        Unknown    5.10.25-linuxkit   containerd://1.4.3-k3s3
```

Because we are using k3d, the "nodes" runs as containers and that can be identified using the docker client:

```
docker ps -f name=k3d
CONTAINER ID   IMAGE                             COMMAND                  CREATED         STATUS         PORTS                                            NAMES
75ed4bf094b2   ghcr.io/k3d-io/k3d-tools:latest   "/app/k3d-tools noop"    2 minutes ago   Up 2 minutes                                                    k3d-kubernetes-cluster-tools
992bfa04a7b7   ghcr.io/k3d-io/k3d-proxy:latest   "/bin/sh -c nginx-pr…"   2 minutes ago   Up 2 minutes   0.0.0.0:80->80/tcp, 127.0.0.1:6445->6443/tcp   k3d-kubernetes-cluster-serverlb
21a2679b5500   rancher/k3s:v1.22.9-k3s1          "/bin/k3d-entrypoint…"   2 minutes ago   Up 2 minutes                                                    k3d-kubernetes-cluster-agent-1
68510b7d1bbb   rancher/k3s:v1.22.9-k3s1          "/bin/k3d-entrypoint…"   2 minutes ago   Up 2 minutes                                                    k3d-kubernetes-cluster-agent-0
00d20e9443f3   rancher/k3s:v1.22.9-k3s1          "/bin/k3d-entrypoint…"   2 minutes ago   Up 2 minutes                                                    k3d-kubernetes-cluster-server-0
```

## Deploy the flask app to kubernetes

Create the deployment:

```
$ kubectl apply -f kubernetes/
service/flask-app-service created
ingress.networking.k8s.io/flask-app-ingress created
deployment.apps/flask-app created
deployment.apps/flask-db created
secret/flask-secrets created
```

View the deployment:

```
$ kubectl get deployments
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
flask-db    1/1     1            1           11m
flask-app   3/3     3            3           11m
```

View the pods:

```
$ kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
flask-db-6c7f76489-nvw5b     1/1     Running   0          12m
flask-app-8485fb56dd-rzq4q   1/1     Running   0          12m
flask-app-8485fb56dd-jzpj8   1/1     Running   0          12m
flask-app-8485fb56dd-vjdhw   1/1     Running   0          12m
```

View the ingress:

```
$ kubectl get ingress
NAME                CLASS    HOSTS                        ADDRESS      PORTS   AGE
flask-app-ingress   <none>   flask-app.127.0.0.1.nip.io   172.20.0.3   80      63s
```

View the services:

```
$ kubectl get service
NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes          ClusterIP   10.43.0.1      <none>        443/TCP   2m57s
flask-app-service   ClusterIP   10.43.142.13   <none>        80/TCP    67s
flask-db            ClusterIP   10.43.104.104  <none>        3306/TCP  64s
```

## Test application on Kubernetes

Test the application on the kubernetes cluster:

```
$ curl http://flask-app.127.0.0.1.nip.io/hostname
hello from flask-app-8485fb56dd-rzq4q
```

View the logs from the pod:

```
$ kubectl logs -f pod/flask-app-8485fb56dd-rzq4q
[2022-06-04 23:13:19 +0000] [7] [INFO] Starting gunicorn 20.0.4
[2022-06-04 23:13:19 +0000] [7] [INFO] Listening at: http://0.0.0.0:8080 (7)
[2022-06-04 23:13:19 +0000] [7] [INFO] Using worker: threads
[2022-06-04 23:13:19 +0000] [9] [INFO] Booting worker with pid: 9
[2022-06-04 23:13:19 +0000] [10] [INFO] Booting worker with pid: 10
10.42.0.3 - - [04/Jun/2022:23:14:45 +0000] "GET /hostname HTTP/1.1" 200 37 "-" "curl/7.54.0"
```

As we have set the replica count to 3, we should see 3 different responses from 3 requests:

```
$ for each in $(seq 1 3) ; do curl http://flask-app.127.0.0.1.nip.io/hostname; echo "" ; done
hello from flask-app-8485fb56dd-rzq4q
hello from flask-app-8485fb56dd-jzpj8
hello from flask-app-8485fb56dd-vjdhw
```

## View the database

You can use kubectl to run a mysql pod and connect to it over its service name, first decode the password secret:

```bash
# on macosx
$ password=$(kubectl get secrets/flask-secrets --template={{.data.db_password}} | base64 -D)
# or on linux
$ password=$(kubectl get secrets/flask-secrets --template={{.data.db_password}} | base64 -d)
```

The connect to the database:

```bash
$ kubectl run -it --rm --image=mysql:8.0 --restart=Never mysql-client -- mysql --host flask-db.default.svc.cluster.local --user=ruan  --password=$password

mysql> 
```

## Seed the database

Seed the database with sample data, for docker:

```
docker run --rm -i --network=public -e API_HOST=flask-app:8080 loadimpact/k6 run --quiet - < k6lib/post.js
```

And for kubernetes:

```
docker run --rm -i --net=host -e API_HOST=flask-app.127.0.0.1.nip.io loadimpact/k6 run --quiet - < k6lib/post.js
```

## Clean up

Terminate the cluster via k3d:

```
k3d cluster delete --all
```

Or terminate the cluster via terraform:

```
terraform -chdir=infra destroy -auto-approve
```

## Resources

Docker:
- https://docs.docker.com/get-docker/

K3d:
- https://k3d.io/stable/

Terraform k3d Provider:
- https://registry.terraform.io/providers/pvotal-tech/k3d/latest

K6:
- https://k6.io/docs/using-k6/http-requests/
