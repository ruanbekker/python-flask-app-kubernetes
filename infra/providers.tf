terraform {
  required_providers {
    k3d = {
      source = "pvotal-tech/k3d"
      version = "0.0.7"
    }
  }
}

provider "k3d" {
  # Configuration options
}
