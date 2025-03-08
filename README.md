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
    └── Data Processing
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
└── Models
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
    │   └── Infer_Model.py   
    │
    └── Remote_Sensing_Deforestation_Model
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

The dataset, approximately 565 MB in size, was collected from the following source: (1).
  
**2. For the LLM-RAG Model**  
We compiled detailed bird information from seven authoritative sources: (2), (3), (4), (5), (6), (7), and (8). The dataset consists of nine integrated text files (one per species) and forty-seven bird images. Due to copyright considerations, we only included abstracts from Google Scholar (Source 8) rather than full scientific articles.
  
**3. For the Remote Sensing Model**  
We obtained time series data of remote sensing Landsat images, detailing global forest extent and annual change from 2000 to 2023, from source (9), along with more than 20,000 georeferenced data from previous locations where the nine species were observed since the early 1980s, although without audio recordings, as provided by source (3).

<br>
All data is stored in a private Google Cloud Bucket (https://console.cloud.google.com/storage/browser/acoustic_monitoring_project;tab=objects?hl=en&project=gen-lang-client-0083231133&prefix=&forceOnObjectsSortingFiltering=false)
       
    
         

<br><br>
## Data Pipeline Containers
1. One container processes the forty-seven images by resizing and storing them back to Google Cloud Storage (GCS).

	**Input:** Source and destination GCS locations, resizing parameters, and required secrets (provided via Docker).

	**Output:** Resized images stored in the specified GCS location.

2. Another container prepares data for the RAG model, including tasks such as chunking, embedding, and populating the vector database.

<br><br>
## Data Pipeline Overview

1. **`src/datapipeline/preprocess_cv.py`**
   This script handles preprocessing on the forty-seven bird images. It reduces the image sizes to 128x128 to ensure faster loading, improved performance, and a consistent display. The preprocessed dataset is stored in the specified GCS location.

2. **`src/datapipeline/preprocess_rag.py`**
   This script prepares the necessary data for setting up our vector database. It performs chunking, embedding, and loads the data into a vector database (ChromaDB).

3. **`src/datapipeline/Pipfile`**
   We used the following packages to help with preprocessing:
   - `special cheese package`

4. **`src/preprocessing/Dockerfile(s)`**
   Our Dockerfiles follow standard conventions, with the exception of some specific modifications described in the Dockerfile/described below.

<br><br>
## Running Dockerfile
Instructions for running the Dockerfile can be added here.
To run Dockerfile - `Instructions here`

**Models container**
- This container has scripts for model training, rag pipeline and inference
- Instructions for running the model container - `Instructions here`

**Notebooks/Reports**
This folder contains code that is not part of container - for e.g: Application mockup, EDA, any 🔍 🕵️‍♀️ 🕵️‍♂️ crucial insights, reports or visualizations.


<br><br>
## Data Versioning Strategy

An initial baseline of both the acoustic data and the LLM-RAG data was collected on [XXX]. The data was scraped from the sources mentioned above using custom scripts, with some websites requiring logins for access.

Over the course of several months, additional data may be incorporated into both the acoustic and LLM-RAG datasets. However, for the remote sensing model, deforestation data is typically updated once per year.

Both the acoustic and LLM-RAG datasets are dynamic, with snapshots taken at specific intervals to capture full replacements of the data. As website authors may update or expand the data, these datasets are expected to evolve over time, with content updates occurring over several months.

Previous versions of the models are not expected to be revisited. Given that updates are anticipated to occur every few months, the team will establish the initial baseline and later implement the Data Versioning Container.

----
