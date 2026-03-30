variable "project_id" {
  description = "The GCP Project ID where resources will be created"
  type        = string
  # Leave empty, populate in terraform.tfvars or via -var="project_id=..."
}

variable "region" {
  description = "Region for GCP resources"
  type        = string
  default     = "us-central1" # Free tier friendly
}

variable "firestore_location" {
  description = "Firestore database location"
  type        = string
  default     = "nam5" # Multi-region US (includes us-central1)
}
