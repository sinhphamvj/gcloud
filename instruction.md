
export PROJECT_BUCKET=qwiklabs-gcp-00-fe7a9dc6763c

python3 analyze-images-v2.py qwiklabs-gcp-00-fe7a9dc6763c YOUR_BUCKET_NAME


1. Tạo Service Account
gcloud iam service-accounts create ml-sa-account \
  --display-name "Service Account for ML, BQ, GCS"


gcloud projects add-iam-policy-binding qwiklabs-gcp-00-fe7a9dc6763c \
  --member="serviceAccount:ml-sa-account@qwiklabs-gcp-00-fe7a9dc6763c.iam.gserviceaccount.com" \
  --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding qwiklabs-gcp-00-fe7a9dc6763c \
  --member="serviceAccount:ml-sa-account@qwiklabs-gcp-00-fe7a9dc6763c.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"


  export GOOGLE_APPLICATION_CREDENTIALS="/home/student-00-506c1271fb42/ml-sa-key.json"
  or export GOOGLE_APPLICATION_CREDENTIALS=/home/$(whoami)/ml-sa-key.json

2.Tạo và tải về file credentials (JSON)
gcloud iam service-accounts keys create ~/ml-sa-key.json \
  --iam-account=ml-bq-storage-sa@qwiklabs-gcp-00-fe7a9dc6763c.iam.gserviceaccount.com

//Cấu hình biến môi trường cho Python script
  export GOOGLE_APPLICATION_CREDENTIALS="~/ml-sa-key.json"
  echo $GOOGLE_APPLICATION_CREDENTIALS

export PROJECT_BUCKET=qwiklabs-gcp-00-fe7a9dc6763c

//copy file script python vao project

gsutil cp gs://qwiklabs-gcp-00-fe7a9dc6763c/analyze-images-v2.py .

// run scrip python
python3 analyze-images-v2.py qwiklabs-gcp-00-fe7a9dc6763c qwiklabs-gcp-00-fe7a9dc6763c


PROJECT_ID=qwiklabs-gcp-00-fe7a9dc6763c
SERVICE_ACCOUNT=ml-bq-storage-sa@$PROJECT_ID.iam.gserviceaccount.com


# Grant BigQuery Data Owner role
gcloud projects add-iam-policy-binding qwiklabs-gcp-00-fe7a9dc6763c \
    --member="serviceAccount:ml-bq-storage-sa@qwiklabs-gcp-00-fe7a9dc6763c.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataOwner"

# Grant Storage Admin role
gcloud projects add-iam-policy-binding qwiklabs-gcp-00-fe7a9dc6763c \
    --member="serviceAccount:ml-bq-storage-sa@qwiklabs-gcp-00-fe7a9dc6763c.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding qwiklabs-gcp-00-fe7a9dc6763c \
    --member="serviceAccount:ml-bq-storage-sa@qwiklabs-gcp-00-fe7a9dc6763c.iam.gserviceaccount.com" \
    --role="roles/ml.admin"
gcloud iam service-accounts keys create ~/ml-bq-storage-sa-key.json \
    --iam-account ml-bq-storage-sa@qwiklabs-gcp-00-fe7a9dc6763c.iam.gserviceaccount.com




4. Tạo BigQuery dataset và table

bq --location=US mk -d images

bq mk -t images.results \
file_name:STRING,original_text:STRING,detected_lang:STRING,translated_text:STRING


Tạo Dataset image_classification_dataset
curl -X POST \
  -H "Authorization: Bearer $OAUTH2_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "datasetReference": {
      "datasetId": "image_classification_dataset",
      "projectId": "YOUR_PROJECT_ID"
    },
    "location": "US"
  }' \
  "https://bigquery.googleapis.com/bigquery/v2/projects/YOUR_PROJECT_ID/datasets"
Thay YOUR_PROJECT_ID = qwiklabs-gcp-03-667e2626aefb (hoặc project của bạn).

$OAUTH2_TOKEN là access token của service account. Bạn có thể lấy bằng:
gcloud auth application-default print-access-token

Tạo Table image_text_detail

curl -X POST \
  -H "Authorization: Bearer $OAUTH2_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tableReference": {
      "projectId": "YOUR_PROJECT_ID",
      "datasetId": "image_classification_dataset",
      "tableId": "image_text_detail"
    },
    "schema": {
      "fields": [
        {"name": "description", "type": "STRING"},
        {"name": "locale", "type": "STRING"},
        {"name": "translated_text", "type": "STRING"},
        {"name": "file_name", "type": "STRING"}
      ]
    }
  }' \
  "https://bigquery.googleapis.com/bigquery/v2/projects/YOUR_PROJECT_ID/datasets/image_classification_dataset/tables"
Chú ý: Table chỉ được tạo nếu dataset đã tồn tại.

Token $OAUTH2_TOKEN vẫn là access token của service account với quyền bigquery.admin.