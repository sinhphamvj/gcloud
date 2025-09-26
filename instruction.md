

1. Tạo Service Account : thay tên qwiklabs vào các lệnh dưới

gcloud iam service-accounts create ml-sa-account \
  --display-name "Service Account for ML, BQ, GCS"


gcloud projects add-iam-policy-binding qwiklabs-gcp-00-97242c5698cf \
  --member="serviceAccount:ml-sa-account@qwiklabs-gcp-00-97242c5698cf.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding qwiklabs-gcp-00-97242c5698cf \
  --member="serviceAccount:ml-sa-account@qwiklabs-gcp-00-97242c5698cf.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataOwner"

gcloud projects add-iam-policy-binding qwiklabs-gcp-00-97242c5698cf \
  --member="serviceAccount:ml-sa-account@qwiklabs-gcp-00-97242c5698cf.iam.gserviceaccount.com" \
  --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding qwiklabs-gcp-00-97242c5698cf \
  --member="serviceAccount:ml-sa-account@qwiklabs-gcp-00-97242c5698cf.iam.gserviceaccount.com" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding qwiklabs-gcp-00-97242c5698cf \
  --member="serviceAccount:ml-sa-account@qwiklabs-gcp-00-97242c5698cf.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

## sau khi cấp quyề xong chờ 2 phút rồi check completed task 1

2.Tạo và tải về file credentials (JSON)
gcloud iam service-accounts keys create ~/ml-sa-key.json \
  --iam-account=ml-sa-account@qwiklabs-gcp-00-97242c5698cf.iam.gserviceaccount.com

##Cấu hình biến môi trường cho Python script
  export GOOGLE_APPLICATION_CREDENTIALS=/home/$(whoami)/ml-sa-key.json
  export BUCKET_NAME=qwiklabs-gcp-00-97242c5698cf
  export PROJECT_NAME=qwiklabs-gcp-00-97242c5698cf

##copy file script python vao project

  gsutil cp gs://qwiklabs-gcp-00-97242c5698cf/analyze-images-v2.py .

## run scrip python ( chú ý thay tên qwiklabs theo project)
  python3 analyze-images-v2.py qwiklabs-gcp-00-97242c5698cf qwiklabs-gcp-00-97242c5698cf

*** chú ý khi chạy script python theo yêu cầu của baì lab translate ra ngôn ngữ nào có thể là : en fr ja 