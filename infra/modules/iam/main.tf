variable "project_id" { type = string }

# 1. Service Account for the Backend (even if it runs on Hetzner, it needs GCP credentials)
resource "google_service_account" "backend_sa" {
  account_id   = "tuber-backend-sa"
  display_name = "Service Account for TubeRPG Backend (Hetzner)"
}

# 2. IAM Roles
resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

resource "google_project_iam_member" "secret_viewer" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

# 3. Secret Manager (for GEMINI_API_KEY)
resource "google_secret_manager_secret" "gemini_key" {
  secret_id = "GEMINI_API_KEY"
  
  replication {
    auto {}
  }
}

# Output the Service Account email for the user
output "service_account_email" {
  value = google_service_account.backend_sa.email
}
