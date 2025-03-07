
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


#source - ebird.org
def extract_data(URL, FILE_PATH):
    if not os.path.exists(FILE_PATH):
        print('downloading data...')
        result = requests.get(URL)
        html = result.text
        with open(FILE_PATH, 'w') as f:
            f.write(html)
            print('written data')
    else:
        print('loading data from file...')
        with open(FILE_PATH, 'r') as f:
            html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find("div", class_="content-column one_half").text
    print(rows)

    return rows


def save_doc(text, doc_path):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(doc_path)

def all_urls(spec_name,urls, main_fold):
    for specie, url in zip(spec_name,urls):
       
        path = os.path.join(main_fold, specie)
        os.makedirs(path, exist_ok=True)
        file_name = 'data.html'
        file_path = os.path.join(path, file_name)

        data = extract_data(url, file_path)
        bucket_name = "acoustic_monitoring_project"   
        # folder_prefix = "bird_images"
        folder_prefix2 = "peru_aves_descriptions"

        blob_name = f"{folder_prefix2}/{specie.replace(' ', '_')}.txt"
        # upload_to_gcs(bucket_name, f'{folder_prefix}/{specie}_{i + 1}.jpg', img_p) 

        upload_to_gcs(bucket_name, blob_name, data)
        # upload_to_gcs(bucket_name, f'{folder_prefix2}/{specie}_{i + 1}.jpg', img_p) 



species = ["Rupicola peruvianus",
           "Aulacorhynchus coeruleicinctis",
           "Doliornis sclateri",
           "Pipile cumanensis",
           "Gallinago jamesoni",
           "Tinamus osgoodi",
           "Pionus tumultuosus",
           "Hapalopsittaca melanotis"
           ]
urls = ["https://www.peruaves.org/cotingidae/andean-cock-rock-rupicola-peruvianus/",
        "https://www.peruaves.org/ramphastidae/blue-banded-toucanet-aulacorhynchus-coeruleicinctis/",
        "https://www.peruaves.org/cotingidae/bay-vented-cotinga-doliornis-sclateri/",
        "https://www.peruaves.org/cracidae/blue-throated-piping-guan-pipile-cumanensis/",
        "https://www.peruaves.org/scolopacidae/andean-snipe-gallinago-jamesoni/",
        "https://www.peruaves.org/tinamidae/black-tinamou-tinamus-osgoodi/",
        "https://www.peruaves.org/psittacidae/speckle-faced-parrot-pionus-tumultuosus/",
        "https://www.peruaves.org/psittacidae/black-winged-parrot-hapalopsittaca-melanotis/"
]
mainpath = 'bird_files2'

all_urls(species, urls,mainpath)

