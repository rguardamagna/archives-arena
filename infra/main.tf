terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# --- 1. APIS (Manual enable or via TF) ---
# NOTE: It's often safer to enable these once via gcloud, 
# but we can declare them here for completeness.
resource "google_project_service" "firestore" {
  service = "firestore.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "secretmanager" {
  service = "secretmanager.googleapis.com"
  disable_on_destroy = false
}

# --- 2. FIRESTORE ---
module "firestore" {
  source   = "./modules/firestore"
  project_id = var.project_id
  location = var.firestore_location
  
  depends_on = [google_project_service.firestore]
}

# --- 3. IAM & SECRETS ---
module "iam" {
  source     = "./modules/iam"
  project_id = var.project_id
  
  depends_on = [google_project_service.secretmanager]
}
