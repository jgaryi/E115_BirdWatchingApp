
import requests
import os
from bs4 import BeautifulSoup
from docx import Document
from PIL import Image
from io import BytesIO


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
    rows = soup.find("p", class_="u-stack-sm").text
    print(rows)
    # img_url = soup.find('img', class_="Species-media-image")["src"]
    img_url = [img["src"] for img in soup.find_all("img", class_="Species-media-image")]
    print(img_url)
    img_list = []
    for i in img_url:
        img = requests.get(i)
        img_list.append(Image.open(BytesIO(img.content)))
        
    # img = requests.get(img_url)
    # print(img)
    return rows, img_list

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

        data, images = extract_data(url, file_path)

        doc_p = os.path.join(path, f'{specie}.docx')
        save_doc(data, doc_p)

        for i, image in enumerate(images):
            img_p = os.path.join(path, f'{specie}_{i + 1}.jpg')
            image.save(img_p)
       
        

species = ["Rupicola peruvianus",
           "Andigena hypoglauca",
           "Aulacorhynchus coeruleicinctis",
           "Doliornis sclateri",
           "Pipile cumanensis",
           "Gallinago jamesoni",
           "Tinamus osgoodi",
           "Pionus menstruus",
           "Hapalopsittaca melanotis"
           ]
urls = ["https://ebird.org/species/andcot1",
        "https://ebird.org/species/gybmot1",
        "https://ebird.org/species/blbtou1",
        "https://ebird.org/species/bavcot1",
        "https://ebird.org/species/butpig1",
        "https://ebird.org/species/andsni1",
        "https://ebird.org/species/blatin1",
        "https://ebird.org/species/blhpar1",
        "https://ebird.org/species/blwpar1"
]
mainpath = 'bird_files'

all_urls(species, urls,mainpath)
