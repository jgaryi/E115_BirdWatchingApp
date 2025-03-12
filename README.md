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
├── Notebooks
│   └── Acoustic_Monitoring_EDA.ipynb
├── References
├── Reports
│   └── Statement_of_Work.pdf
│   └── E115_BirdWatching App Wireframe.pdf
│   └── birdwatchingapp_vm_screenshot.png
└── src
    └── Acoustic_Monitoring_Model
    │   ├── Dockerfile
    │   ├── pipfile
    │   ├── pipfile.lock
    │   └── Infer_Model.py
    │   
    └── LLM-RAG_Model
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
This project aims to develop an AI-powered bird identification and knowledge application, using the Yanachaga Chemillen National Park in Peru as a case study. The app will offer two primary methods for bird recognition: (1) users can upload a sound file for automatic identification, powered by an acoustic AI model, or (2) manually search for a bird by its scientific name using a dropdown menu to select from one of nine species.<br>

If the identified bird is one of the 500 species found in the national park but not listed in the dropdown menu, the app will display only the species name and return to the initial page when clicked again. If the bird is one of the nine pre-selected species—whose populations are vulnerable and decreasing—the app will provide detailed information about the species, its migratory path, and an image for visual reference. <br>

An interactive map will show the bird's previously identified locations within the national park, habitat details, and changes over time that help explain why these species are vulnerable or endangered. The map will also highlight other areas where the bird is likely to be found, based on predictions from a geo-referenced model using remote sensing data. Additionally, a built-in chatbot will allow users to ask bird-related questions and receive answers powered by a Large Language Model with Retrieval-Augmented Generation (LLM-RAG).
<br><br>

# Milestone 2

In this milestone, we present the components for data management, as well as the acoustic, RAG-LLM, and remote sensing models.

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

The dataset, approximately 565 MB in size, was collected from the following source: [**1**](https://xeno-canto.org/about/xeno-canto). The data will be used for building a transfer learning model based on base BirdNet model to improve the accuracy of species prediction using the acoustic data collected by users.
  
**2. For the LLM-RAG Model**  
We compiled detailed bird information from three authoritative sources: [**2**](https://www.peruaves.org/), [**3**](https://ebird.org/home), [**4**](https://en.wikipedia.org/wiki/Main_Page).
The dataset consists of nine integrated text files (one per species) and forty-seven bird images.
  
**3. For the Remote Sensing Model**  
We obtained more than 20,000 georeferenced data from previous locations where the nine species were observed since the early 1980s, although without audio recordings, from source [**3**](https://ebird.org/home). We will obtain (time series) data from remote sensing images, detailing forest extent and annual change and other habitat and biodiversity characteristics from source [**5**](https://developers.google.com/earth-engine/datasets). 

<br>
The data for the acoustic model and LLM-RAG model is stored in a private Google Cloud Storage (GCS) bucket, while remote sensing and geo-referenced data is stored in Google Earth Engine, a cloud-based platform for geospatial data processing and analysis.
       
    
         

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


<br><br>
## Running Dockerfiles
Instructions for running the Dockerfiles:

**Data Collection**
[`data/data_collection/Dockerfile`](data/data_collection/Dockerfile)  
- Run the `docker-shell.sh` to launch the container.
- Create a `secrets` folder at the same level with the `cli.py` file 
- Add your GCS credentials to the `secrets` folder and rename the jason file to `acoustic_monitoring_sa`
- Run the `cli.py` within the container.
- Run the `preprocess_cv.py` within the container.
- The processed images and text files will be stored in your GCS bucket.

**Data Processing**
[`data/data_processing/Dockerfile`](data/data_processing/Dockerfile)  
- Run the `docker-shell.sh` to launch the container.  
- Create a `secrets` folder at the same level with the `cli.py` file  
- Add your GCS credentials to the `secrets` folder  
- Run `python cli.py --chunk --chunk_type char-split` in the container
- Run `python cli.py --chunk --chunk_type recursive-split` in the container
- Run `python cli.py --embed --chunk_type char-split` in the container
- Run `python cli.py --embed --chunk_type recursive-split` in the container


**Models container**  
   1. Acoustic Inference Model - use the existing BirdNet model for inference 
   [`src/models/acoustic_model/Dockerfile`](src/models/acoustic_model/Dockerfile)
   - Run `docker-shell.sh` to launch the container
   - Run `Species_Prediction.py` within the container
   
   2. Accoustic Transfer Training Model
    - Not available yet. We will use data from the nine representative bird species previously mentioned to perform transfer learning and enhance the prediction confidence of the model for the bird species of interest. The transfer learning model will be ready in the next milestone.

   3. LLM-RAG Model - [`src/models/llm-rag/Dockerfile`](src/models/llm-rag/Dockerfile)
- In the container:  
- Run `python cli.py --load --chunk_type char-split`  
- Run `python cli.py --load --chunk_type recursive-split`  
- Run `python cli.py --query --chunk_type char-split`  
- Run `python cli.py --query --chunk_type recursive-split`  
- Run `python cli.py --chat --chunk_type char-split`  
- Run `python cli.py --chat --chunk_type recursive-split`  

  Note: The query prompts are:
  -	"Where does Andigena hypoglauca live?"

4. Remote Sensing Model - [`src/models/remote_sensing_model/Dockerfile`](src/models/remote_sensing_model/Dockerfile)
- Create or sign in a Google Earth Engine Account   
- Before running the script, you need to authenticate your Google Earth Engine account. To do this, run the following Python code:  
	import ee  
	ee.Authenthicate()   
- The ee.Authenticate() method will output a URL to the console. It will look something like this:   
	Go to the following link in your browser:   
	https://accounts.google.com/o/oauth2/auth?client_id=...  
- When you open this URL in a web browser, it will ask you to log in your Google Earth Engine account.  
- Run the `docker-shell.sh` to launch the container.  
- Run the `birdlocations.py` within the container  

Currently, the Python script identifies the locations of the bird, with remote sensing images in the background that include key habitat characteristics such as deforestation and biodiversity indicators. Future milestones will build on this foundation to develop a map that identifies other areas where the bird is likely to be found, based on predictions from a geo-referenced AI model using the remote sensing data.

<br><br>
## Notebooks/Reports
The Jupyter file `Acoustic_Monitoirng_EDA` explore the features of audio file. The audio signal or data can be represented in time, frequency and time-frequency domain. The time and frequency domain represenation only show information of audio signal from one-dimension. while the time-frequency domain representation will give a 2D representation as an image. The Mel spectrogram can be extracted from this 2D image and fed as input to Convolutional Neural Networks for model training and prediction.    

<br><br>

## Virtual Machine (VM) Setup
-	Create a VM Instance from GCP
-	SSH into your newly created instance
-	Update OS packages: sudo apt-get update
-	Install Git: sudo apt install git
<br><br>

## Data Versioning Strategy

An initial baseline of both the acoustic data and the LLM-RAG data was collected in March 2025. The data was scraped from the sources mentioned above using custom scripts.

Over the course of several months, additional data may be incorporated into both the acoustic and LLM-RAG datasets. However, for the remote sensing model, relevant information such as deforestation changes is typically updated once per year.

Both the acoustic and LLM-RAG datasets are dynamic, with snapshots taken at specific intervals to capture full replacements of the data. As website authors may update or expand the data, these datasets are expected to evolve over time, with content updates occurring over several months.

Previous versions of the models are not expected to be revisited. Given that updates are anticipated to occur every few months, the team will establish the initial baseline and later implement the Data Versioning Container.

----
