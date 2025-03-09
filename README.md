## Project Milestone 2 - E115 - Birdwatching App
   
#### Project Milestone 2 Organization

```
├── Readme.md
└── Data
    └── Data_Collection
    │   ├── Dockerfile
    │   ├── pipfile
    │   ├── pipfile.lock
    │   ├── docker-shell.sh
    │   ├── cli.py
    │   └── preprocess_cv.py
    │
    └── Data_Processing
    │   ├── Dockerfile
    │   ├── pipfile
    │   ├── pipfile.lock
    │   └── preprocess_rag.py
├── Notebooks
│   └── Acoustic_Monitoring_EDA.ipynb
├── References
├── Reports
│   └── Statement_of_Work.pdf
│   └── E115_BirdWatching App Wireframe.pdf
└── src
    └── Acoustic_Monitoring_Model
    │   ├── Dockerfile
    │   ├── pipfile
    │   ├── pipfile.lock
    │   └── Infer_Model.py
    │   
    └── RAG_Model
    │   ├── Dockerfile
    │   ├── pipfile
    │   ├── pipfile.lock
    │   └── cli.py   
    │
    └── Remote_Sensing_Model
        ├── Dockerfile
        ├── pipfile
        ├── pipfile.lock
        └── Infer_Model.py
```

# E115 - Birdwatching App

**Team Members:** Jaqueline Garcia-Yi, Susan Urban, Yong Li, and Victoria Okereke

**Group Name:** Birdwatching App

**Project:**  
This project aims to develop an AI-powered bird identification and knowledge application using as case study the the Yanachaga Chemillen National Park in Peru. The app will offer two primary methods for bird recognition: (1) users can upload a sound file for automatic identification, driven by an acoustic AI model, or (2) manually search for a bird by its scientific name. <br><br>
Upon successful identification, the app will present comprehensive information about the bird, including its geographic location within the national park, key species characteristics, and a corresponding image for visual reference. The integrated map will also display the bird's current habitat conditions, highlighting changes such as deforestation through a remote sensing model. <br><br>
Additionally, a built-in chatbot will enable users to ask bird-related questions, providing expert answers powered by a LLM Retrieval-Augmented Generation (LLM-RAG) model.
<br><br>

# Milestone 2

In this milestone, we present the components for data management, as well as the acoustic, language, and remote sensing models.

## Data  
**1. For the Acoustic Model**  
We gathered a dataset of 411 audio recordings of nine representative bird species located inside the National Park:  
- Andigena hypoglauca, 64
- Aulacorhynchus coeruleicinctis, 27
- Doliornis sclateri, 11
- Gallinago jamesoni, 56
- Hapalopsittaca melanotis, 11
- Pionus tumultuosus, 15
- Pipile cumanensis, 49
- Rupicola peruvianus, 158
- Tinamus osgoodi, 20  

The dataset, approximately 565 MB in size, was collected from the following source: [**1**](https://xeno-canto.org/about/xeno-canto)
  
**2. For the LLM-RAG Model**  
We compiled detailed bird information from three authoritative sources: [**2**](https://www.peruaves.org/), [**3**](https://ebird.org/home), [**4**](https://en.wikipedia.org/wiki/Main_Page).
The dataset consists of nine integrated text files (one per species) and forty-seven bird images.
  
**3. For the Remote Sensing Model**  
We obtained time series data of remote sensing Landsat images, detailing global forest extent and annual change from 2000 to 2023, from source (9), along with more than 20,000 georeferenced data from previous locations where the nine species were observed since the early 1980s, although without audio recordings, as provided by source (3).

<br>
All data is stored in a private Google Cloud Storage Bucket (https://console.cloud.google.com/storage/browser/acoustic_monitoring_project;tab=objects?hl=en&project=gen-lang-client-0083231133&prefix=&forceOnObjectsSortingFiltering=false)
       
    
         

<br><br>
## Data Pipeline Containers
The data pipeline consists of two containers:
1. **data_collection** contains scripts that automate the collection, processing, and storage of our data, including text, images, and audio.

	**Input:** Url pages from the authoritative sources above.

	**Output:** Resized images, merged texts, and audio files stored in the specified GCS location.

2. **data_processing** prepares data for the RAG model, including tasks such as chunking, embedding, and populating the vector database.

<br><br>
## Data Pipeline Overview

1. **`data/data_collection/cli.py`**
   This script scrapes text and images from three websites and stores the data both locally and in GCS bucket. It handles the following:
   1.	Text Data -> Saved as `.txt` files in the `bird_description` folder.
   2.	Image Data -> Stored in the `bird_images` folder.
   3.	Audio Data -> Manually added to the `acoustic_data` folder.

2. **`data/data_collection/preprocess_cv.py`** This script process the images collected in `bird_images` by:
   1.	Resizing them to 128x128 pixels to ensure faster loading, improved performance, and consistent display in the app.
   2.	Uploading the resized images to the `resized` folder in the specified GCS location.
4. **`data/data_processing/preprocess_rag.py`**
   This script prepares the necessary data for setting up our vector database. It performs chunking, embedding, and loads the data into a vector database (ChromaDB).

<br><br>
## Running Dockerfiles
Instructions for running the Dockerfiles:

**Data Collection**
[`data/data_collection/Dockerfile`](data/data_collection/Dockerfile)  
- Run the `docker-shell.sh` to launch the container.
- Create a `secrets` folder at the same level with the `cli.py` file
- Add your GCS credentials to the `secrets` folder
- Run the `cli.py` within the container.
- Run the `preprocess_cv.py` within the container.
- The processed images and text files will be stored in your GCS bucket.

**Data Processing**
[`data/data_processing/Dockerfile`](data/data_processing/Dockerfile)  
- [PLACEHOLDER]
- [PLACEHOLDER]


**Models container**
- This container has scripts for model training, rag pipeline and inference
- Instructions for running the model container - `Instructions here`
   1. Acoustic Inference Model - use the existing BirdNet model for inference 
   ['src/models/acoustic_model/Dockerfile'](src/models/acoustic_model/Dockerfile)
    - Run the `docker-shell.sh` to launch the container
    - Run the `Species_Prediction.py` within the container
   
   2. Transfer Training Model
    - We will use data of nine representative bird species mentioned above to do transfer learning and improve the prediction confidence of the model to bird species we are interested. The transfer learning model will be ready in the next mileston.  

**Notebooks/Reports**
This folder contains code that is not part of container - for e.g: Application mockup, EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.
- The Jupyter file `Acoustic_Monitoirng_EDA` explore the features of audio file. The audio signal or data can be represented in time, frequency and time-frequency domain. The time and frequency domain represenation only show information of audio signal from one-dimension. while the time-frequency domain representation will give a 2D representation as an image. The Mel spectrogram can be extracted from this 2D image and fed as input for Convolutional Neural Network.    

<br><br>
## Data Versioning Strategy

An initial baseline of both the acoustic data and the LLM-RAG data was collected on [XXX]. The data was scraped from the sources mentioned above using custom scripts, with some websites requiring logins for access.

Over the course of several months, additional data may be incorporated into both the acoustic and LLM-RAG datasets. However, for the remote sensing model, deforestation data is typically updated once per year.

Both the acoustic and LLM-RAG datasets are dynamic, with snapshots taken at specific intervals to capture full replacements of the data. As website authors may update or expand the data, these datasets are expected to evolve over time, with content updates occurring over several months.

Previous versions of the models are not expected to be revisited. Given that updates are anticipated to occur every few months, the team will establish the initial baseline and later implement the Data Versioning Container.

----
