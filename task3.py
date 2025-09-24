import sys
import io
from google.cloud import storage
from google.cloud import vision
from google.cloud import translate_v2 as translate
from google.cloud import bigquery

def main(project_id, bucket_name):
    # Init clients
    storage_client = storage.Client(project=project_id)
    vision_client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()
    bq_client = bigquery.Client(project=project_id)

    bucket = storage_client.bucket(bucket_name)

    # BigQuery table reference (bạn cần có dataset 'images' và table 'results')
    dataset_id = f"{project_id}.images"
    table_id = f"{dataset_id}.results"

    files = storage_client.list_blobs(bucket_name)

    rows_to_insert = []

    for file in files:
        if not file.name.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        print(f"Processing file: {file.name}")
        content = file.download_as_bytes()

        # --- OCR with Vision API ---
        image = vision.Image(content=content)
        response = vision_client.document_text_detection(image=image)

        if response.error.message:
            print(f"Vision API error: {response.error.message}")
            continue

        if response.text_annotations:
            extracted_text = response.text_annotations[0].description
        else:
            extracted_text = ""

        # --- Translation API ---
    

        # --- Save text file back to bucket ---
        txt_blob = bucket.blob(file.name + ".txt")
        txt_blob.upload_from_string(extracted_text, content_type="text/plain")

        print(f"Saved text to {file.name}.txt in bucket {bucket_name}")

       


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 analyze-images-v2.py <PROJECT_ID> <BUCKET_NAME>")
        sys.exit(1)

    project_id = sys.argv[1]
    bucket_name = sys.argv[2]

    main(project_id, bucket_name)

