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

    # BigQuery table reference (bạn cần có dataset 'image_classification_dataset' và table 'image_text_detail')
    dataset_id = f"{project_id}.image_classification_dataset"
    table_id = f"{dataset_id}.image_text_detail"

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
        target_lang = "en"
        detected_lang = "und"
        translated_text = extracted_text

        if extracted_text.strip() != "":
            detection = translate_client.detect_language(extracted_text)
            detected_lang = detection.get("language")

            if detected_lang != "en":
                translation = translate_client.translate(extracted_text, target_language=target_lang)
                translated_text = translation["translatedText"]

        # --- Save text file back to bucket ---
        txt_blob = bucket.blob(file.name + ".txt")
        txt_blob.upload_from_string(translated_text, content_type="text/plain")

        print(f"Saved OCR/translated text to {file.name}.txt in bucket {bucket_name}")

        # --- Prepare row for BigQuery ---
        rows_to_insert.append({
            "description": extracted_text,
            "locale": detected_lang,
            "translated_text": translated_text,
            "file_name": file.name
        })

    # --- Insert rows into BigQuery ---
    if rows_to_insert:
        errors = bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors == []:
            print("New rows added to BigQuery successfully.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 analyze-images-v2.py <PROJECT_ID> <BUCKET_NAME>")
        sys.exit(1)

    project_id = sys.argv[1]
    bucket_name = sys.argv[2]

    main(project_id, bucket_name)
