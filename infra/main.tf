resource "k3d_cluster" "cluster" {
  name    = "kubernetes-cluster"
  servers = 1
  agents  = 2

  kube_api {
    host      = "k3d-master.127.0.0.1.nip.io"
    host_ip   = "127.0.0.1"
    host_port = 6445
  }

  image   = "rancher/k3s:${var.k3s_version}"
  network = "k3d-network"
  token   = "k3dSuperSecretToken"

  port {
    host_port      = 8080
    container_port = 80
    node_filters = [
      "loadbalancer",
    ]
  }

  label {
    key   = "foo"
    value = "bar"
    node_filters = [
      "agent[1]",
    ]
  }

  k3d {
    disable_load_balancer = false
    disable_image_volume  = false
  }

  kubeconfig {
    update_default_kubeconfig = true
    switch_current_context    = true
  }

}
