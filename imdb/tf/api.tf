variable "gcp_service_list" {
  type        = list(string)
  description = "The list of apis necessary for the project"
  default     = [ "storage.googleapis.com"]
}


# locals {
#   all_project_services = concat(var.gcp_service_list, [
#     "serviceusage.googleapis.com",
#     "iam.googleapis.com",
#   ])
# }

# resource "google_project_service" "enabled_apis" {
#   project  = var.project_id
#   for_each = toset(locals.all_project_services)
#   service  = each.key

#   disable_on_destroy = false
# }


resource "google_project_service" "enabled_apis" {
  project  = var.project_id
#   for_each = toset(locals.all_project_services)
  for_each = toset([
    "cloudresourcemanager.googleapis.com",
    "serviceusage.googleapis.com",
    "iam.googleapis.com",
  ])
  service  = each.key

  disable_on_destroy = false
}
