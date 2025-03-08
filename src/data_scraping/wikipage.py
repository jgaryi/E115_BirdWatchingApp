
import requests
import os
from bs4 import BeautifulSoup
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


#source - wikipedia
def extract_data(URL, FILE_PATH):
    if not os.path.exists(FILE_PATH):
        print('downloading data...')
        result = requests.get(URL)
        html = result.content
        with open(FILE_PATH, 'wb') as f:
            f.write(html)
            print('written data')
    else:
        print('loading data from file...')
        with open(FILE_PATH, 'r') as f:
            html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    rows = soup.find("div", class_="mw-content-ltr mw-parser-output")
    # print(rows)
    rows = rows.find_all('p')
    rows = [row.get_text() for row in rows]
    rows = '\n'.join(rows)
    return rows

def all_urls(spec_name,urls, main_fold):
    for specie, url in zip(spec_name,urls):
       
        path = os.path.join(main_fold, specie)
        os.makedirs(path, exist_ok=True)
        file_name = 'data.html'
        file_path = os.path.join(path, file_name)

        data = extract_data(url, file_path)
        bucket_name = "acoustic_monitoring_project"   
        folder_prefix2 = "wiki_data"

        blob_name = f"{folder_prefix2}/{specie.replace(' ', '_')}.docx"

        upload_to_gcs(bucket_name, blob_name, data)
    


species = ["Rupicola peruvianus",
           "Andigena hypoglauca",
           "Aulacorhynchus coeruleicinctis",
           "Doliornis sclateri",
           "Pipile cumanensis",
           "Gallinago jamesoni",
           "Tinamus osgoodi",
           "Pionus tumultuosus",
           "Hapalopsittaca melanotis"
           ]
urls = ["https://en.wikipedia.org/wiki/Andean_cock-of-the-rock",
        "https://en.wikipedia.org/wiki/Grey-breasted_mountain_toucan",
        "https://en.wikipedia.org/wiki/Blue-banded_toucanet",
        "https://en.wikipedia.org/wiki/Bay-vented_cotinga",
        "https://en.wikipedia.org/wiki/Blue-throated_piping_guan",
        "https://en.wikipedia.org/wiki/Jameson%27s_snipe",
        "https://en.wikipedia.org/wiki/Black_tinamou",
        "https://en.wikipedia.org/wiki/Plum-crowned_parrot",
        "https://en.wikipedia.org/wiki/Black-winged_parrot"
        
]
mainpath = 'bird_files_wiki'

all_urls(species, urls,mainpath)

