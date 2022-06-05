# flask-app-kubernetes

Deploy Python Flask app to Kubernetes (k3d)

## Steps

Build the application locally:

```
$ docker-compose up -d --build
```

Test locally:

```
$ curl http://flask-app.127.0.0.1.nip.io:8082
hello from 32c76a0d3784
```

View the logs locally:

```
$ docker-compose logs -f
Attaching to flask-demo-app
flask-demo-app    | [2022-06-04 23:04:59 +0000] [8] [INFO] Starting gunicorn 20.0.4
flask-demo-app    | [2022-06-04 23:04:59 +0000] [8] [INFO] Listening at: http://0.0.0.0:8080 (8)
flask-demo-app    | [2022-06-04 23:04:59 +0000] [8] [INFO] Using worker: threads
flask-demo-app    | [2022-06-04 23:04:59 +0000] [10] [INFO] Booting worker with pid: 10
flask-demo-app    | [2022-06-04 23:04:59 +0000] [11] [INFO] Booting worker with pid: 11
flask-demo-app    | 172.19.0.1 - - [04/Jun/2022:23:05:13 +0000] "GET / HTTP/1.1" 200 23 "-" "curl/7.54.0"
```

Terminate the application locally:

```
$ docker-compose down
Stopping flask-demo-app ... done
Removing flask-demo-app ... done
```

Builld and push the images to your registry:

```
$ docker-compose build
$ docker-compose push
```

Create a k3d (kubernetes on docker using k3s) kubernetes cluster:

```
$ k3d cluster create --config k3d-cluster.yml
INFO[0061] Cluster 'kubernetes-cluster' created successfully!
```

Check if the nodes are visible:

```
$ kubectl get nodes --output wide
NAME                              STATUS   ROLES                  AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE   KERNEL-VERSION     CONTAINER-RUNTIME
k3d-kubernetes-cluster-agent-0    Ready    <none>                 78s   v1.20.4+k3s1   172.20.0.4    <none>        Unknown    5.10.25-linuxkit   containerd://1.4.3-k3s3
k3d-kubernetes-cluster-agent-1    Ready    <none>                 77s   v1.20.4+k3s1   172.20.0.5    <none>        Unknown    5.10.25-linuxkit   containerd://1.4.3-k3s3
k3d-kubernetes-cluster-server-0   Ready    control-plane,master   99s   v1.20.4+k3s1   172.20.0.3    <none>        Unknown    5.10.25-linuxkit   containerd://1.4.3-k3s3
```

Create the deployment:

```
$ kubectl apply -f deployment.yml
service/flask-app-service created
ingress.networking.k8s.io/flask-app-ingress created
deployment.apps/flask-app created
```

View the deployment:

```
$ kubectl get deployments
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
flask-app   3/3     3            3           54s
```

View the pods:

```
$ kubectl get pods
NAME                         READY   STATUS    RESTARTS   AGE
flask-app-676cb766f5-td8cc   1/1     Running   0          58s
flask-app-676cb766f5-4d8wp   1/1     Running   0          58s
flask-app-676cb766f5-nnj7s   1/1     Running   0          58s
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
```

Test the application on the kubernetes cluster:

```
$ curl http://flask-app.127.0.0.1.nip.io:8080
hello from flask-app-676cb766f5-4d8wp
```

View the logs from the pod:

```
$ kubectl logs -f pod/flask-app-676cb766f5-4d8wp
[2022-06-04 23:13:19 +0000] [7] [INFO] Starting gunicorn 20.0.4
[2022-06-04 23:13:19 +0000] [7] [INFO] Listening at: http://0.0.0.0:8080 (7)
[2022-06-04 23:13:19 +0000] [7] [INFO] Using worker: threads
[2022-06-04 23:13:19 +0000] [9] [INFO] Booting worker with pid: 9
[2022-06-04 23:13:19 +0000] [10] [INFO] Booting worker with pid: 10
10.42.0.3 - - [04/Jun/2022:23:14:45 +0000] "GET / HTTP/1.1" 200 37 "-" "curl/7.54.0"
```

Terminate the cluster:

```
k3d cluster delete --all
```
