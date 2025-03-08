from google.cloud import storage
from PIL import Image
import io
import os
from google.oauth2 import service_account


image_location = "bird_files"  
GCBucket_name = "birdwatchingapp"
image_size = (128, 128) 

def list_local_images(directory):
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('jpg')):
                image_files.append(os.path.join(root, file))
    print(f"Image files found: {image_files}")
    return image_files


def resize_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB") 
        img = img.resize(image_size, Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="JPEG")  # Convert all to JPEG for consistency
        buf.seek(0)
        return buf

def upload_to_gcs(file_name, image_buffer, bucket_name):
    credentials = service_account.Credentials.from_service_account_file('birdwatchingapp_sa.json')

    storage_client = storage.Client(credentials=credentials, project='birdwatchingapp_sa')
    bucket = storage_client.bucket(bucket_name)

    b_name = os.path.basename(file_name)
    gc_blob_name = f"resized/{b_name}"
    blob = bucket.blob(gc_blob_name)
    image_buffer.seek(0)
    blob.upload_from_file(image_buffer, content_type="image/jpeg")

    print(f"Uploaded: {gc_blob_name}")

def process_local_images():
    if not os.path.exists(image_location):
        print(f"Error: Directory '{image_location}' not found.")
        return

    images = list_local_images(image_location)
    if not images:
        print("No images found in the local directory.")
        return

    for image_name in images:
        resized_image_buffer = resize_image(image_name)
        upload_to_gcs(image_name, resized_image_buffer, GCBucket_name)

if __name__ == "__main__":
    process_local_images()
