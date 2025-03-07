import requests
import os
from bs4 import BeautifulSoup
from docx import Document
from PIL import Image
from io import BytesIO
from google.cloud import storage
from google.oauth2 import service_account

def upload_to_gcs(bucket_name, blob_name, content):

    credentials = service_account.Credentials.from_service_account_file('acoustic_monitoring_sa.json')

    storage_client = storage.Client(credentials=credentials, project='acoustic_monitoring_sa')
    bucket = storage_client.bucket(bucket_name)
    
    
    blob = bucket.blob(blob_name)
    blob.upload_from_string(content)
    print(f'Uploaded data to gs://{bucket_name}/{blob_name}')

# source - birdsoftheworld.com
def extract_BOTW(URL):
    print('Downloading data...')
    result = requests.get(URL)
    html = result.text
    soup_botw = BeautifulSoup(html, 'html.parser')
    sections = soup_botw.find_all("section", class_="u-stack-lg u-text-4-loose u-article")
    all_paragraphs = []
    for sec in sections:
        paragraphs = sec.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            print(text)
            all_paragraphs.append(text)
    return all_paragraphs

def save_doc_to_bytes(text_list):
    doc = Document()
    for text in text_list:
        doc.add_paragraph(text)
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io.getvalue()

def all_urls(spec_names, urls, bucket_name):
    for specie, url in zip(spec_names, urls):
        # Download and extract text in memory
        paragraphs = extract_BOTW(url)
        # Save DOCX to memory as bytes
        doc_bytes = save_doc_to_bytes(paragraphs)
        # Upload the DOCX bytes to Google Cloud Storage
        # blob_name = f"{specie}/{specie}.docx"
        folder_prefix2 = "birdsoftheworld"
        # blob_name = f"{specie}/{specie}.txt"
        blob_name = f"{folder_prefix2}/{specie.replace(' ', '_')}.docx"
        upload_to_gcs(bucket_name, blob_name, doc_bytes)

# List of species and corresponding URLs
species = [
    "Rupicola peruvianus",
    "Andigena hypoglauca",
    "Aulacorhynchus coeruleicinctis",
    "Doliornis sclateri",
    "Pipile cumanensis",
    "Gallinago jamesoni",
    "Tinamus osgoodi",
    "Pionus menstruus",
    "Hapalopsittaca melanotis"
]

urls = [
    "https://birdsoftheworld.org/bow/species/andcot1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/gybmot1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/blbtou1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/bavcot1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/butpig1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/andsni1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/blatin1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/blhpar1/cur/introduction",
    "https://birdsoftheworld.org/bow/species/blwpar1/cur/introduction"
]

main_folder = 'botw_files'
# Replace 'YOUR_BUCKET_NAME' with your actual Google Cloud bucket name
bucket_name = "acoustic_monitoring_project" 

all_urls(species, urls, bucket_name)
