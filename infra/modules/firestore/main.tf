variable "project_id" { type = string }
variable "location" { type = string }

resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)" # Native Firestore default name
  location_id = var.location
  type        = "FIRESTORE_NATIVE"
  
  delete_protection_state = "DELETE_PROTECTION_DISABLED" # Change for production!
  deletion_policy         = "DELETE"
}
